import socket
import icmplib
import platform
import os
import sys

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow


def write_icmp_to_file(final_route, output_file):
    with open(output_file, 'w+') as f:
        for data in final_route:
            print(data, file=f)
    print(R + '\t[->]' + Y + 'Result have been saved in the file {}'.format(output_file))


def icmp_route(ip, output):
    if platform.system == 'Linux':
        if os.geteuid() != 0:
            print(R+'[-]'+C+ ' Root Privilege is needed for Traceroute..!!!')
            sys.exit()

    result=icmplib.traceroute(ip, count=1)
    print(G+'\n[*] '+R+'Looking for Traceroot...')
    final_route = []
    print('\n' + R + 'HOPS'.ljust(7) + 'IP'.ljust(17) + 'HOST' + W + '\n')
    for entry in result:
        hop_index=str(entry._distance)
        hop_addr=entry._address
        try:
            hop_host = socket.gethostbyaddr(hop_addr)[0]
        except socket.herror:
            hop_host = 'Unknown'

        print(G + hop_index.ljust(7) + C + hop_addr.ljust(17) + W + hop_host)
        final_route.append(hop_index.ljust(7) + hop_addr.ljust(17) + hop_host)

    write_icmp_to_file(final_route, output)
    print(R+'-'*20)
