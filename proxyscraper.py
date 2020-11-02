#!/usr/bin/env python3.9
from bs4 import BeautifulSoup
import requests
import random
import sys
import os

chain_mode = "random_chain"
line_ending = "\r\n"
valid_types = [ 'http', 'https', 'socks4', 'socks5']
valid_anonymity = ['elite', 'anonymous', 'transparent']
max_timeout = 10000

if len(sys.argv) == 6:
	proxy_type = str(sys.argv[1])
	proxy_timeout = str(sys.argv[2])
	proxy_country = str(sys.argv[3])
	proxy_anonymity = str(sys.argv[4])
	proxy_num = int(sys.argv[5])
elif len(sys.argv) == 3:
	proxy_type = str(sys.argv[1])
	proxy_num = int(sys.argv[2])
	proxy_timeout = 10000
	proxy_country = "all"
	proxy_anonymity = "elite"
else:
	print(f"""Usage:
{sys.argv[0]} [type] [timeout] [country] [anonymity] [proxy num]
{sys.argv[0]} [type] [proxy num]

Defaults:
Type =			( http, https, socks4, socks5 )
Timeout = 10000ms	( <= 10000ms )
Country = all		Country 2-letter code
Anonymity = elite	( elite, anonymous, transparent)
""")
	exit(0)

# Check if arguments are invalid
if not proxy_type in valid_types:
	print(f"Invalid proxy type: {proxy_type}")
	exit(1)
if not proxy_anonymity in valid_anonymity:
	print(f"Invalid anonymity: {proxy_anonymity}")
	exit(1)
if int(proxy_timeout) > max_timeout:
	print(f"Invalid timeout: {proxy_timeout}")
	exit(1)

base_url = "https://api.proxyscrape.com/?request=getproxies&"

url = base_url + f"proxytype={proxy_type}&timeout={proxy_timeout}&country={proxy_country}"

if proxy_type == "http":
	url += f"&ssl=no&anonymity={proxy_anonymity}"

if proxy_type == "https":
	url += f"&ssl=yes&anonymity={proxy_anonymity}"

# Get the proxies
proxies = []
tmp = requests.get(url).text.split(line_ending)
if proxy_num == 0:
	proxies = tmp
	proxy_num = len(proxies)
else:
	for i in range(proxy_num):
		proxies.append(tmp[random.randint(0,len(tmp)-1)])

for i in range(proxy_num):
	if proxies[i] == "":
		proxies.pop(i)

print(f"Got: {proxy_num} {proxy_type} proxies")

try:
	os.mkdir("raw")
except FileExistsError:
	pass

# Write the raw file
raw_file = open(f"raw/{proxy_num}-{proxy_type}.txt","w")
conf = open(f"{proxy_num}-{proxy_type}.conf","w")
conf.write(f"{chain_mode}\n")
conf.write("quiet_mode\n")
conf.write("proxy_dns\n")
conf.write("remote_dns_subnet 224\n")
conf.write("tcp_read_time_out 10000\n")
conf.write("tcp_connect_time_out 10000\n")
conf.write("[ProxyList]\n")

for i in range(len(proxies)):
	raw_file.write(proxies[i] + "\n")
	tmp = proxies[i].replace(':','\t')
	if tmp == "":
		continue
	conf.write(f"{proxy_type}\t{tmp}\n")

raw_file.close()
conf.close()