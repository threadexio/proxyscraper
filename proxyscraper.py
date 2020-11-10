#!/usr/bin/env python3.9
from bs4 import BeautifulSoup
import threading
import requests
import argparse

proxy_types = [ 'http', 'https' ]
anonymity_levels = [ 'elite', 'anonymous', 'transparent' ]

print("""
   ██▓███   ██▀███   ▒█████  ▒██   ██▒▓██   ██▓  ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  ▓█████  ██▀███  
  ▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒▒ █ █ ▒░ ▒██  ██▒▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
  ▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒░░  █   ░  ▒██ ██░░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
  ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░ ░ █ █ ▒   ░ ▐██▓░  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄\tBy threadexio
  ▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░▒██▒ ▒██▒  ░ ██▒▓░▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒\ton Github
  ▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░   ██▒▒▒ ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░░   ░▒ ░ ▓██ ░▒░ ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
  ░░         ░░   ░ ░ ░ ░ ▒   ░    ░   ▒ ▒ ░░  ░  ░  ░  ░          ░░   ░   ░   ▒   ░░          ░     ░░   ░ 
              ░         ░ ░   ░    ░   ░ ░           ░  ░ ░         ░           ░  ░            ░  ░   ░     
                                       ░ ░              ░                                                    
""")

parser = argparse.ArgumentParser()
parser.add_argument("type", help="Proxy type (http, https)", type=str)
parser.add_argument("-n", help="Number of proxies to get", type=int, default=0)
parser.add_argument("-a", help="Anonymity level (transparent, anonymous, default: elite)", type=str, default="elite")
parser.add_argument("-o", help="Output file (default: proxies.txt)", type=str, default="proxies.txt")
args = parser.parse_args()

proxy_type = args.type
proxy_num = args.n
proxy_anonymity = args.a

global proxy_list
proxy_list = []

if proxy_type not in proxy_types:
    print(f"Unknown proxy type: {proxy_type}")
    exit(1)

if proxy_anonymity not in anonymity_levels:
    print(f"Unknown anonymity level: {proxy_anonymity}")
    exit(1)

# proxyscrape.com
def proxyscrape():
    baseurl = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&"
    if proxy_type == "https":
        url = baseurl + f"ssl=yes&anonymity={proxy_anonymity}&simplified=true"
    elif proxy_type == "http":
        url = baseurl + f"ssl=no&anonymity={proxy_anonymity}&simplified=true"
    r = requests.get(url)
    if r.status_code == 200:
        for proxy in r.text.splitlines():
            proxy_list.append(f"{proxy}")

# sslproxies.org && free-proxy-list.net && us-proxy.org
def scrapeproxies(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text,"html.parser")
    else:
        return None
    rows = soup.find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all('td')
        https = cells[-2].text.lower()
        anonymity = cells[-4].text.lower()
        if proxy_anonymity in anonymity:
            if (proxy_type == "http" and https == "yes") or (proxy_type == "https" and https == "no"):
                continue
            proxy_list.append(f"{cells[0].text}:{cells[1].text}")
        else:
            continue

# proxy-list.download
def proxylist(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text,"html.parser")
    else:
        return None
    rows = soup.find("tbody", attrs={"id":"tabli"}).find_all("tr")
    for row in rows:
        cells = row.find_all('td')
        anonymity = cells[-2].text.lower()
        if proxy_anonymity in anonymity:
            proxy_list.append(f"{cells[0].text}:{cells[1].text}")

########################################################################################################

if proxy_type == "http":
    threading.Thread(target=proxyscrape).start()
    threading.Thread(target=scrapeproxies, args=("https://sslproxies.org/",)).start()
    threading.Thread(target=scrapeproxies, args=("https://free-proxy-list.net/",)).start()
    threading.Thread(target=scrapeproxies, args=("https://us-proxy.org/",)).start()
    threading.Thread(target=proxylist, args=("https://www.proxy-list.download/HTTP",)).start()

if proxy_type == "https":
    threading.Thread(target=proxyscrape).start()
    threading.Thread(target=scrapeproxies, args=("https://sslproxies.org/",)).start()
    threading.Thread(target=scrapeproxies, args=("https://free-proxy-list.net/",)).start()
    threading.Thread(target=scrapeproxies, args=("https://us-proxy.org/",)).start()
    threading.Thread(target=proxylist, args=("https://www.proxy-list.download/HTTPS",)).start()

for t in threading.enumerate():
    try:
        t.join()
    except RuntimeError:
        continue

# Write the file
output = open(args.o,'w')
for proxy in proxy_list:
    output.write( f"{proxy}\n" )
output.close()