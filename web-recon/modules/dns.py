import os
from dnslib import DNSRecord
import socket
import tldextract

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow


def write_dns_to_file(final_dns, final_dmarc, output_file):
    with open(output_file, 'w+') as f:
        for data in final_dns:
            print(data, file=f)

        for data in final_dmarc:
            print(data, file=f)
    print(R + '\t[->]' + Y + 'Result have been saved in the file {}'.format(output_file))


def dns_enum(target, output):
    final_dns=[]
    final_result=[]
    url_parts=tldextract.extract(target)
    target=".".join(url_parts[-2:])

    print(G+'\n[+]'+R+' Starting DNS Enumeration\n')
    types=['A','AAAA', 'CNAME', 'MX', 'NS', 'TXT']
    forward_addr=('8.8.8.8', 53)
    client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for type in types:
        q = DNSRecord.question(target, type)
        client.sendto(bytes(q.pack()), forward_addr)
        data, _ = client.recvfrom(1024)
        d = DNSRecord.parse(data)
        d=str(d).split('\n')
        final_result.extend(d)

    final_result=set(final_result)

    for each_dns in final_result:
        if each_dns.startswith(';') == False:
            final_dns.append(each_dns)

    if len(final_dns) != 0:
        for entry in final_dns:
            print(G+'[+] '+C+f'{entry}')
    else:
        print(R+'[!] DNS Record Not found..!!!')

    dmarc_target='_dmarc.'+target
    q = DNSRecord.question(dmarc_target, 'TXT')
    packet = q.send('8.8.8.8', 53, tcp='UDP')
    dmarc_answer = DNSRecord.parse(packet)
    dmarc_answer = str(dmarc_answer).split('\n')
    final_dmarc=[]

    for each_dmarc in dmarc_answer:
        if each_dmarc.startswith('_dmarc') == True:
            final_dmarc.append(each_dmarc)

    if len(final_dmarc) != 0:
        for entry in final_dmarc:
            print(G+'[+] '+C+f'{entry}')
        print(R+'-'*20)

    else:
        print(Y+'[!]'+R+'DMARC Record Not found..!!!')

    write_dns_to_file(final_dns, final_dmarc, output)
