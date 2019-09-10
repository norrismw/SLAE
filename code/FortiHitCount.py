#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import time
from netmiko import ConnectHandler


## used regardless of choice; used in gen_commands() and get_count()
# generates list of policies

def get_policies():
    policy_string = net_connect.send_command('show firewall policy | grep edit')
    return [int(s) for s in policy_string.split() if s.isdigit()]


## used regardless of choice; used in clear_count() and messy_list()
# generates list of commands based on choice of show/clear and list of policies

def gen_commands():
    gen_commands = []
    for policy_id in get_policies():
        gen_commands.append(base_command + ' ' + str(policy_id))
    return gen_commands


## used if choice == "clear"
# sends the list of generated clear commands

def clear_count():
    for command in gen_commands():
        print(command)
        # net_connect.send_command(command)

## used if choice == "show"; used in clean_list()
# generates messy list from output of show commands; used in clean_list()

def messy_list():
    messy_list = []
    for command in gen_commands():
        time.sleep(1)
        messy_list.append(net_connect.send_command(command))
    return messy_list


## used if choice == "show"
# cleans messy list; used in get_count()

def clean_list():
    clean_list = []
    for command_output in messy_list():
        hits_true = re.findall(r'hit count:\d+', command_output)
        if len(hits_true) == 0:
            clean_list.append('0')
        else:
            hit_count = re.findall(r'\d+', hits_true[0])
            clean_list.append(hit_count[0])
    return clean_list


## used if choice == "show"
# combines the keys (policy ids) with the hit counts (for each policy) into a dict

def get_count():
    keys = get_policies()
    values = clean_list()
    hit_counts = dict(zip(keys, values))
    return hit_counts


# this will be a configuration file in practice

fortigate = {
    'device_type': 'fortinet',
    'host': '',
    'username': '',
    'password': '',
    'port': 22, # optional, defaults to 22
    'secret': '', # optional, defaults to ''
    }

choice = sys.argv[1]

# logic to determine which commands should be generated/sent

if choice == 'clear':
    base_command = 'di firewall iprope clear 100004'
elif choice == 'show':
    base_command = 'di firewall iprope show 100004'
else:
    sys.exit(1)

net_connect = ConnectHandler(**fortigate)

if choice == 'clear':
    clear_count()
else:
    get_count()

net_connect.disconnect()
