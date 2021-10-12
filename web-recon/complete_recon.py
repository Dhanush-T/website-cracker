import requests
import sys
import ipaddress
from urllib.parse import urlparse
import argparse
import socket
import importlib

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow


def banner():
    print("""
     ______   ____   _____   _____   ___     _
    |  __  \ | ___| |  ___| |  _  | |   \   | |
    | |__) / | |__  | |     | | | | | |\ \  | |
    |  _  /  | ___| | |     | | | | | | \ \ | |
    | | \ \  | |__  | |___  | |_| | | |  \ \| |
    |_|  \_\ |____| |_____| |_____| |_|   \___|  \n""")



def requirement():
	with open('requirement.txt', 'r') as f:
		pkg_list = f.read().strip().split('\n')
		fail=False
		for pkg in pkg_list:
			s = importlib.util.find_spec(pkg)
			if s is None:
				print(R+'[!] '+C+f'Package {pkg} is not installed')
				fail=True
			else:
				pass
		if fail==True:
			print(R+'[*] Run command: '+C+'pip3 install -r requirement.txt '+R+'to install alll the packages.')
			sys.exit()


def parse_args():
	parser = argparse.ArgumentParser(description='Recon - Web Recon Tool You Will Need ')
	parser.add_argument('url', help='Taget URL')
	parser.add_argument('--ssl', help='SSL Certificate Info', action='store_true')
	parser.add_argument('--subdom', help='Subdomain Enumeration', action='store_true')
	parser.add_argument('--header', help='Hearder Info', action='store_true')
	parser.add_argument('--trace', help='Traceroute', action='store_true')
	parser.add_argument('--dns', help='DNS Enumeration', action='store_true')
	parser.add_argument('--crawl', help='Website Crawler', action='store_true')
	parser.add_argument('--full', help='Full Recon', action='store_true')
	parser.add_argument('--output',type=str, help='Output to file')

	return parser.parse_args()



if __name__ == '__main__':
	banner()
	requirement()

	args = parse_args()
	target=args.url
	output=args.output
	ssl_info=args.ssl
	subdoms=args.subdom
	header=args.header
	trace=args.trace
	dns=args.dns
	crawler = args.crawl
	full = args.full

	if target.startswith(('http', 'https')) == False:
        	print(R + '[-]' + C + ' Protocol Missing, Include ' + W + 'http://' + C + ' or ' + W + 'https://' + '\n')
        	sys.exit()
	else:
		pass

	if target[-1] == '/':
		target=target[:-1]

	print(R+'[*] Target: '+Y+target)
	hostname=urlparse(target).netloc
	try:
		ipaddress.ip_address(hostname)
		ip=hostname
	except:
		try:
			ip=socket.gethostbyname(hostname)
			print(R+'[*] IP Address: '+Y+ip)
		except:
			print(R+'Unable to resolve the IP')
			sys.exit()

	if subdoms==True:
		from modules.sub_domain import subdomain
		subdomain(target, output)

	if ssl_info==True:
		from modules.ssl_cert import ssl_cert
		ssl_cert(target, output)

	if header==True:
		from modules.header import header_info
		header_info(target, output)

	if trace==True:
		from modules.traceroute import icmp_route
		icmp_route(ip, output)

	if dns==True:
		from modules.dns import dns_enum
		dns_enum(target, output)

	if crawler == True:
		from modules.crawler import crawler
		crawler(target, output)

	if full == True:
		output = output.split('.')
		filename = output[0]

		from modules.ssl_cert import ssl_cert
		ssl_cert(target, filename+'_ssl.txt')

		from modules.header import header_info
		header_info(target, filename+'_header.txt')

		from modules.traceroute import icmp_route
		icmp_route(ip, filename+'_icmp.txt')

		from modules.dns import dns_enum
		dns_enum(target, filename+'_dns.txt')

		from modules.crawler import crawler
		crawler(target, filename+'_crawler.txt')

		from modules.sub_domain import subdomain
		subdomain(target, filename+'_subdoms.txt')
