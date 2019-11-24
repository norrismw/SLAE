#!/usr/bin/python3

from Crypto.Cipher import AES
import hashlib
import random

# Place plaintext shellcode here
shellcode = b'SHELLCODE_PLACEHOLDER'


# Generates 128 bit (16 byte) key 
def md5_key(key):
    b_key = str.encode(key)
    hashed_key = hashlib.md5(b_key)
    return hashed_key.hexdigest()


# Formats the shellcode for printing to terminal
def format_shellcode(bytes_obj):
    formatted = ''
    for byte in bytes_obj:
        formatted += '\\x'
        formatted += '%02x' % byte
    return formatted


# Pads the shellcode. AES encryption works on 16 byte blocks
def pad(shellcode):
    if len(shellcode) % 16 != 0:
        c = 16 - (len(shellcode) % 16)
        for i in range(c):
            shellcode += b'*'
    return shellcode


key = input("Key: ") # Takes user-chosen key
key = md5_key(key) # Generates key to 16 byte key
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)]) # Pseudo-random intialization vector
cipher = AES.new(key) # Cipher object for encryption
enc_shellcode = cipher.encrypt(pad(shellcode)) # Encrypted shellcode

print("\n[+] Encrypted shellcode:\n{}".format(format_shellcode(enc_shellcode)))
