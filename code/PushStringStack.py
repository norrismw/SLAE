#!/usr/bin/python
# -*- coding: utf-8 -*-

# PushStringStack.py
# Generates x86 assembly code to store a user-supplied string on the stack & clear any used registers.
# Usage: python PushStringStack.py <string>
# Example: python PushStringStack.py $'Push it good\nPush it real good\nPush it good\P-push it real good\n'
# Note: Don't forget $ on the command line when using characters such as \n and \r!

import sys

string = sys.argv[1]

double_words = len(string) / 4  # how many complete 4 byte chunks (double words)
left_over = len(string) % 4  # how many left over bytes (i.e. n % 4 = 1, 2, or 3)

rev_hex = string[::-1].encode('hex')  # encoded hex string; least significant bytes first
rev_hex_div4 = rev_hex[left_over * 2::]  # a string of n bytes where n % 4 = 0

counter = double_words
start = 0
end = 1

print '[!] String details ... \n'

print '[*] ' + str(double_words) + ' four-byte chunk(s).'
print '[*] ' + str(left_over) + ' left over byte(s).'
print '[*] ' + str(len(string)) + ' total byte(s).\n'

print '[!] Assembly ... \n'

print 'xor edx, edx'
print 'push edx'

if left_over == 1:
    print 'mov dl, 0x' + rev_hex[:left_over * 2]
    print 'push dx'
    print 'xor edx, edx'

if left_over == 2:
    print 'mov dx, 0x' + rev_hex[:left_over * 2]
    print 'push dx'
    print 'xor edx, edx'

if left_over == 3:
    print 'mov dl, 0x' + rev_hex[:2]
    print 'push dx'
    print 'xor ecx, ecx'
    print 'mov cx, 0x' + rev_hex[2:6]
    print 'push cx'
    print 'xor edx, edx'
    print 'xor ecx, ecx'

while counter != 0:
    print 'push 0x' + rev_hex_div4[start * 8:end * 8]
    counter = counter - 1
    start = start + 1
    end = end + 1

print '\n[+] Complete!'
