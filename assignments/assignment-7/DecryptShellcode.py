#!/usr/bin/python3

from Crypto.Cipher import AES
import hashlib
import random

# Place encrypted shellcode here
enc_shellcode = b'ENC_SHELLCODE_PLACEHOLDER'


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


# Removes padding from decrypted shellcode
def unpad_shellcode(shellcode):
    shellcode = format_shellcode(shellcode)
    return shellcode.replace('\\x2a', '')


key = input("Key: ") # Takes user-chosen key
key = md5_key(key) # Generates key to 16 byte key
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)]) # Pseudo-random intialization vector
cipher = AES.new(key) # Cipher object for decryption
dec_shellcode = cipher.decrypt(enc_shellcode) # Decrypted shellcode with padding
shellcode = unpad_shellcode(dec_shellcode) # Decrypted shellcode; no padding

print("\n[+] Shellcode:\n{}".format(shellcode))
