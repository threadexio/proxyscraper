# proxyscraper
Python-based proxy scraper

## What this does:
This script gets the latest available proxy lists from [proxyscrape.com](https://proxyscrape.com)
and compiles them into:
<ul>
	<li>proxychains-ng configuration file format</li>
	<li>general IP:PORT format</li>
</ul>

## Help
```
Usage:
./proxyscraper.py [type] [timeout] [country] [ssl] [anonymity] [proxy num]
./proxyscraper.py [type] [proxy num]

Defaults:
Type =			( http, socks4, socks5 )
Timeout = 10000ms	( <= 10000ms )
Country = all		Country 2-letter code
Anonymity = elite	( elite, anonymous, transparent)

---------------- -------------------------------------------------------------------------------------
type 		|	 Proxy type, can be: http, https, socks4 or socks5
---------------- -------------------------------------------------------------------------------------
timeout 	|	 Connect timeout, must be lower than 10000 (ms)
---------------- -------------------------------------------------------------------------------------
country 	|	 Country 2-letter code (US,GB)
		|	 (see available countries for each type here: https://proxyscrape.com/free-proxy-list)
---------------- -------------------------------------------------------------------------------------
anonymity 	|	 Anonymity level of the proxies, can be: elite, anonymous, transparent
		|	 (recommended: elite)
---------------- -------------------------------------------------------------------------------------
```
