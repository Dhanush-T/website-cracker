import ssl
from urllib.parse import urlparse
import socket


R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow


def write_sub_to_file(result, output_file):
    with open(output_file, 'w+') as f:
        for x, y in result.items():
            data=f'[+] {x}: '+ y
            print(data, file=f)

    print(R + '\t[->]' + Y + 'Result have been saved in the file {}'.format(output_file))



def ssl_cert(url, output):
    resutl=[]
    target = urlparse(url).netloc
    print(G+'\n[*] '+R+'Looking for SSL Cert: ')
    if urlparse(url).scheme == "http":
        port=80
    elif urlparse(url).scheme == "https":
        port=443

    cert = ssl.get_server_certificate((target, port))
    context = ssl.create_default_context()
    socks=socket.socket()
    sock = context.wrap_socket(socks, server_hostname=target)
    sock.connect((target, port))
    certs = sock.getpeercert()

    result={}
    result['siteName']=certs['subject'][0][0][1]
    result['countryName']=certs['issuer'][0][0][1]
    result['organisationName']=certs['issuer'][1][0][1]
    result['commonName']=certs['issuer'][2][0][1]
    result['version']=str(certs['version'])
    result['serialNumber']=certs['serialNumber']
    result['notBefore']=certs['notBefore']
    result['notAfter']=certs['notAfter']
    result['ocsp']=certs['OCSP'][0]
    result['caIssuers']=certs['caIssuers'][0]
    for x, y in result.items():
        print(C+f'\t[+] {x}: '+ G + y)

    write_sub_to_file(result, output)
    print(R+'-'*20)
