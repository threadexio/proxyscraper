#!/usr/bin/env python3.9
from requests.exceptions import *
import threading
import requests
import argparse
import os

proxy_types = [ 'http', 'https' ]

print("""
 ██▓███   ██▀███   ▒█████  ▒██   ██▒▓██   ██▓ ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒▒ █ █ ▒░ ▒██  ██▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒░░  █   ░  ▒██ ██░▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░ ░ █ █ ▒   ░ ▐██▓░▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄\tBy threadexio
▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░▒██▒ ▒██▒  ░ ██▒▓░▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒\ton Github
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░   ██▒▒▒ ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░░   ░▒ ░ ▓██ ░▒░   ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░░         ░░   ░ ░ ░ ░ ▒   ░    ░   ▒ ▒ ░░  ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
            ░         ░ ░   ░    ░   ░ ░     ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                     ░ ░     ░                       ░                               
""")

parser = argparse.ArgumentParser()
parser.add_argument("type", help="Proxy type (http, https)", type=str)
parser.add_argument("file", help="Proxy file", type=str)
parser.add_argument("-u", help="URL to test proxies with (default: google.com)", type=str, default="https://google.com/")
parser.add_argument("-t", help="Number of threads to use (default: 10)", type=int, default=10)
parser.add_argument("-T", help="Timeout for the request in secs (default: 5)", type=int, default=5)
args = parser.parse_args()

proxy_list = []
good_proxies = []

proxy_type = args.type
filename = args.file
threadNum = args.t
timeout = args.T
url = args.u

if proxy_type not in proxy_types:
    print(f"Unknown proxy type: {proxy_type}")
    exit(1)

if not os.access(filename, os.R_OK):
    print(f"Can't read file: {filename}")
    exit(1)

def check(proxy):
    proxyDict = {
        "http" : f"http://{proxy}",
        "https" : f"https://{proxy}"
    }
    try:
        r = requests.get(url, proxies=proxyDict, timeout=timeout)
        return True
    except ProxyError:
        return False
    except Timeout:
        return False

def thread_routine(start):
    i = start
    while True:
        try:
            if check(proxy_list[i]):
                print(proxy_list[i])
                good_proxies.append( proxy_list[i] )
            i += threadNum
        except IndexError:
            break

# Read the file
with open(filename, 'r') as f:
    for line in f.readlines():
        proxy_list.append( line.strip() )
    f.close()

# Create the threads
threadPool = [ threading.Thread(target=thread_routine, args=(i,)) for i in range(threadNum) ]


# Start the threads
for i in range(threadNum):
    threadPool[i].start()

# Wait for the threads to stop
for thread in threading.enumerate():
    try:
        thread.join()
    except RuntimeError:
        pass
