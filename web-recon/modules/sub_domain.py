import requests
import tldextract

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow


def write_sub_to_file(discovered_subs, output_file):
    with open(output_file, 'w+') as f:
        for sub in discovered_subs:
            print(sub, file=f)
    print(R + '\t[->]' + Y + 'Result have been saved in the file {}'.format(output_file))

def subdomain(url, output_file):
    output = output_file
    url_parts=tldextract.extract(url)
    target=".".join(url_parts[1:])

    print(G+"[*] "+R"Looking for subdomains...")
    sub_file = open('subdomains.txt', 'r')
    all_subdomains = sub_file.read()
    subs = all_subdomains.splitlines()
    i = 1
    discovered_subs = []
    for s in subs:
        url = f"https://{s}.{target}"
        try:
            req = requests.get(url)
            if req.status_code == 200:
                print(C+f"\t[+] Discovered URL---> {url}")
                discovered_subs.append(url)
        except requests.ConnectionError:
            pass
        i = i + 1
    write_sub_to_file(discovered_subs, output)
    print(R+'-'*20)
