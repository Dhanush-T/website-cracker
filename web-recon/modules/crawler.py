import os
import re
import bs4
import lxml
import json
import requests
import threading
import tldextract
import urllib

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow

soup = ''
r_url = ''
sm_url = ''
r_total = []
sm_total = []
js_total = []
css_total = []
int_total = []
ext_total = []
img_total = []

result={}


def write_crawl_to_file(final_result, output_file):
	with open(output_file, 'w+') as f:
		for key in final_result:
			print('\n'+key.upper()+' :', file=f)
			for data in final_result[key]:
				print('\t'+data, file=f)
	print(R + '\t[->]' + Y + 'Result have been saved in the file {}'.format(output_file))


def robots(r_url, target):
	global r_total, sm_total, result
	print(G +'[*]'+R+'Looking for robots.txt')

	try:
		r_rqst = requests.get(r_url)
		r_stat_code = r_rqst.status_code

		if r_stat_code == 200:
			print(G+'   [+]'+Y+'Robots Link Found...!!!')
			print(G+'   [+]'+Y+'Extracting robots links....')
			r_page=r_rqst.text
			r_scrape = r_page.split('\n')
			for each_line in r_scrape:
				if each_line.startswith('Allow') or each_line.startswith('Disallow'):
					parts = each_line.split(':')
					condition = parts[0]
					url= parts[1].strip()
					if condition == 'Allow':
						r_link = 'Allowed: '+f'{target}{url}'
						print('\t'+C+r_link)
						r_total.append(r_link)
					elif condition == 'Disallow':
						r_link='Disallow: '+f'{target}{url}'
						r_total.append(r_link)
						print('\t'+C+r_link)

				elif each_line.startswith('Sitemap'):
					parts = each_line.split(':')
					condition = parts[0]
					url= parts[1].strip()
					sm_link = target+url
					sm_total.append(sm_link)

				result['robots'] = r_total
		else:
			print('\t'+C+'[+]'+Y+' No robots.txt file found')
			result['robots'] = ['No robots.txt file found']

	except Exception as e:
		print(R+'[!]'+C+f'Error Occurs: {str(e)}')
		return

	print(R+'-'*20)


def sitemap(sm_url, target):
	global sm_total, result
	print('\n'+G +'[*]'+R+'Looking for sitemap.xml...!!!')
	try:
		sm_rqst = requests.get(sm_url)
		sm_stat_code = sm_rqst.status_code
		if sm_stat_code == 200:
			sm_page = sm_rqst.content
			sm_soup = bs4.BeautifulSoup(sm_page, 'xml')
			links = sm_soup.find_all('loc')
			for url in links:
				url = url.get_text()
				if url != None:
					sm_total.append(url)

			sm_total = set(sm_total)

			if len(sm_total)!= 0:
				print(G+'   [+]'+Y+'Sitemap Found...!!!')
				print(G+'   [+]'+Y+'Extracting links...')
				for link in sm_total:
					print(C+f'\t{link}')

				result['sitemap'] = sm_total
			else:
				print(R+"\t[!] "+Y+"No sitemap links found.")
				result['sitemap'] = ['No sitemap links found.']

		elif sm_stat_code == 404:
			print(C+'\t[!]'+Y+' Not found.')
			result['sitemap'] = ['No sitemap links found.']

		else:
			print(R+f'[!] HTTP Status code is {sm_stat_code}.')
			result['sitemap'] = ['No sitemap links found.']

	except Exception as e:
		print(R+'[!]'+C+f'Error Occurs: {str(e)}')
		return

	print(R+'-'*20)


def css(target, soup):
	global css_total, result
	print(G +'[*]'+R+'Looking for css file...!!!')
	css = soup.find_all('link')

	for link in css:
		url = link.get('href')
		if url!=None and 'css' in url:
			if url.startswith('http'):
				css_total.append(url)
				print(C+f'\t{url}')
			else:
				complete_url = urllib.parse.urljoin(target, url)
				css_total.append(complete_url)
				print(C+f'\t{complete_url}')

	result['css']=css_total
	if len(css_total) == 0:
		print(C+'\t[!]'+Y+' No CSS file found.')
		result['css'] = ['No css links found.']
	print(R+'-'*20)


def js(target, soup):
	global js_total, result
	print(G +'[*]'+R+'Looking for Javascript files...!!!')
	js = soup.find_all('scripts')

	for link in js:
		url = link.get('src')
		if url!=None and '.js' in url:
			if url.startswith('http'):
				js_total.append(url)
				print(C+f'\t{url}')
			else:
				complete_url = urllib.parse.urljoin(target, url)
				js_total.append(url)
				print(C+f'\t{complete_url}')
	result['js'] = js_total

	if len(js_total) == 0:
		print(C+'\t[!]'+Y+' No JavaScript file found.')
		result['js'] = ['No js file found.']
	print(R+'-'*20)


def internal_link(target, soup):
	global int_total, result
	print(G +'[*]'+R+'Looking for any internal links available or not...!!!')

	domain = tldextract.extract(target).registered_domain
	links = soup.find_all('a')
	for link in links:
		url = link.get('href')
		if url!=None:
			if domain in url:
				int_total.append(url)
	int_total=set(int_total)

	if len(int_total)!=0:
		print(R+'   [!]'+Y+'Extracting internal links.')
		for i in int_total:
			print(C+f'\t{i}')
		result['internal_link'] = int_total
	else:
		print(R+'   [!] No internal links found.')
		result['internal_link'] = ['No internal links found.']

	print(R+'-'*20)


def external_link(target, soup):
	global ext_total, result
	print(G +'[*]'+R+'Looking for any external links available or not...!!!')

	domain = tldextract.extract(target).registered_domain
	links = soup.find_all('a')
	for link in links:
		url = link.get('href')
		if url!=None:
			if domain not in url and 'http' in url:
				ext_total.append(url)
	ext_total=set(ext_total)

	if len(ext_total)!=0:
		print(R+'   [!]'+Y+'Extracting external links.')
		for i in ext_total:
			print(C+f'\t{i}')

		result['external_link'] = ext_total
	else:
		print(R+'   [!] No external links found.')
		result['external_link'] = ['No external links found.']

	print(R+'-'*20)


def images(target, soup):
	global img_total, result
	print(G +'[*]'+R+'Looking for any image links available or not...!!!')
	images = soup.find_all('img')

	for link in images:
		url = link.get('src')
		if url!=None:
			if url.startswith('http'):
				img_total.append(url)
			else:
				complete_url = urllib.parse.urljoin(target, url)
				img_total.append(complete_url)
	img_total=set(img_total)
	if len(img_total) != 0:
		print(R+'   [!]'+Y+'Extracting image links.')
		for i in img_total:
			print(C+f'\t{i}')
		result['images'] = img_total
	else:
		print(R+'   [!] No external links found.')
		result['images'] = ['No image links found.']


def crawler(target, output):
	global soup, result
	print('\n' +Y+'[!]'+R+' Starting Crawler....!!!!\n')
	url=urllib.parse.urlparse(target)

	target = url.scheme+'://'+url.netloc
	try:
		rqst=requests.get(target)
	except Exception as e:
		print(R+'[!]'+C+f'Error Occurs: {str(e)}')
		return

	stat_code = rqst.status_code
	if stat_code == 200:
		page = rqst.content
		soup = bs4.BeautifulSoup(page, 'lxml')

		r_url = target+'/robots.txt'
		sm_url = target+'/sitemap.xml'

		robots(r_url, target)
		sitemap(sm_url, target)
		css(target, soup)
		js(target, soup)
		internal_link(target, soup)
		external_link(target, soup)
		images(target, soup)

		write_crawl_to_file(result, output)
	else:
		print(R+'[-]'+Y+f'Status {stat_code}')
	
	print(R+'-'*20)
