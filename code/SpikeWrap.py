#!/usr/bin/python
# -*- coding: utf-8 -*-

# Basic wrapper for generic_send_tcp - needs work!

import sys
import os
import subprocess
import multiprocessing
from multiprocessing import Pool

RHOST = sys.argv[1]
RPORT = sys.argv[2]

all_files = sorted(os.listdir(sys.argv[3]))
spk_files = []

for this_file in all_files:
    if this_file.endswith('.spk'):
        spk_files.append(this_file)

FNULL = open(os.devnull, 'w')

agents = multiprocessing.cpu_count() * 2
step = 1


def generic_send_tcp(spk_file):
    print '[*] Using file: ' + spk_file
    subprocess.call([
        '/usr/bin/generic_send_tcp',
        RHOST,
        RPORT,
        spk_file,
        '0',
        '0',
        ], stdout=FNULL, stderr=FNULL)


with Pool(processes=agents) as pool:
    pool.map(generic_send_tcp, spk_files, step)
