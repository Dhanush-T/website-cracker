#!/usr/bin/env python3

import requests

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow


def write_sub_to_file(result, output_file):
    with open(output_file, 'w+') as f:
        for data in result:
            print(data, file=f)
        print(R + '\t[->]' + Y + 'Result have been saved in the file {}'.format(output_file))


def header_info(url, output):
    result = []
    header_banner = '\n' +G+'[*] '+R+ 'Headers :'
    print(header_banner)
    result.append(header_banner+'\n')
    try:
        rqst = requests.get(url)
        for k, v in rqst.headers.items():
            info = G + '\t[+]' + C + ' {} : '.format(k) + W + v
            print(info)
            result.append(info+'\n')
        write_sub_to_file(result, output)
        print(R+'-'*20)
    except Exception as e:
        print(R+f"Error occurs: {e}")
        pass
