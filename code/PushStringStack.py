#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PushStringStack.py
# Generates x86 assembly code to store a user-supplied string on the stack & clear any used registers.
# Usage: python PushStringStack.py <string>
# Example: python PushStringStack.py $'Push it good\nPush it real good\nPush it good\P-push it real good\n'
# Note: If this is to be used with execve, make sure to include a space at the end of your string; i.e. $'/usr/bin/ls -lah '
# Note: Don't forget $ on the command line when using characters such as \n and \r!

# TODO: command line options when running, i.e. 'execve' or 'no execve' 
# TODO: regarding above comment, if execve, append space at end of user-supplied string
# TODO: provide option for which character should be replaced; this will default to replacing \x20 (space) characters

import binascii
import sys

string = sys.argv[1]

## elementary functions
def reverse_hex(string):
    return binascii.hexlify(string[::-1].encode()).decode() # encoded hex string; least significant bytes first


def count_string(string):
    count_list = []
    count_list.append(len(string) // 4) # double words; how many complete 4 byte chunks (double words)
    count_list.append(len(string) % 4) # left over bytes; how many left over bytes (i.e. n % 4 = 1, 2, or 3)
    return count_list


def replace_count(string):
    return [i for i, x in enumerate(string) if x == ' ']


def rev_hex_div4():
    return reverse_hex(string)[count_string(string)[1] * 2::] # a string of n bytes where n % 4 = 0


## core print functions
def push_string_stack():
    start = 0
    end = 1
    print('xor edx, edx')
    print('push edx')
    if count_string(string)[1] == 1: # 1 left over bytes
        print('mov dl, 0x' + reverse_hex(string)[:count_string(string)[1] * 2])
        print('push dx')
        print('xor edx, edx')
    if count_string(string)[1] == 2: # 2 left over bytes
        print('mov dx, 0x' + reverse_hex(string)[:count_string(string)[1] * 2])
        print('push dx')
        print('xor edx, edx')
    if count_string(string)[1] == 3: # 3 left over bytes
        print('mov dl, 0x' + reverse_hex(string)[:2])
        print('push dx')
        print('xor ecx, ecx')
        print('mov cx, 0x' + reverse_hex(string)[2:6])
        print('push cx')
        print('xor edx, edx')
        print('xor ecx, ecx')
    for x in range(0, count_string(string)[0]):
        print('push 0x' + rev_hex_div4()[start * 8:end * 8])
        start = start + 1
        end = end + 1


def prepare_stack_string():
    print('xor edx, edx')
    a = -1 
    b = -2
    if not count_string(string)[1] % 2: # if there are 0 or 2 left over bytes
        print('mov byte [ebp-5], dl') # replaces terminating \x20 with \x00
        base = 5
    else: # if there are 1 or 3 left over bytes
        print('mov byte [ebp-6], dl') # replaces terminating \x20 with \x00
        base = 6
    for x in range(0, len(replace_count(string))- 1): # replaces the rest of \x20 with \x00
        print('mov byte [ebp-' + str(replace_count(string)[a] - replace_count(string)[b] + base) + '], dl')
        base += replace_count(string)[a] - replace_count(string)[b]
        b = b - 1
        a = a - 1


def push_argv():
    base = 4
    print('xor ebx, ebx') # \0\0\0\0
    print('push ebx') # \0\0\0\0 NULL terminates argv[]
    if count_string(string)[1] == 0: # zero left over bytes
        leftover_push = 0
        base += (leftover_push * 2)
        for x in range(0, len(replace_count(string)) - 1):
            print('lea ebx, [ebp-8]')
            print('push ebx')
        print('lea ebx, [ebp-' + str((count_string(string)[0] * 4) + base) + ']')
        print('push ebx')
    elif count_string(string)[1] == 3: # three left over bytes
        leftover_push = 2
        base += (leftover_push * 2)
        for x in range(0, len(replace_count(string)) - 1):
            print('lea ebx, [ebp-12]')
            print('push ebx')
        print('lea ebx, [ebp-' + str((count_string(string)[0] * 4) + base) + ']')
        print('push ebx')
        print('xor ecx, ecx')
    else: # 1 or 2 left over bytes
        leftover_push = 1
        base += (leftover_push * 2)
        for x in range(0, len(replace_count(string)) - 1):
            print('lea ebx, [ebp-10]')
            print('push ebx')
        print('lea ebx, [ebp-' + str((count_string(string)[0] * 4) + base) + ']')
        print('push ebx')
    print('mov ecx, esp') # pointer to argv[] for 'char *const argv[]'
    print('lea edx, [ebp-4]') # \0\0\0\0 for 'char *const envp[]'


## formatting functions
def string_details():
    print('[!] String details ... \n')
    print('[*] ' + str(count_string(string)[0]) + ' four-byte chunk(s).')
    print('[*] ' + str(count_string(string)[1]) + ' left over byte(s).')
    print('[*] ' + str(len(string)) + ' total byte(s).\n')
    print('[!] Assembly ... \n')
