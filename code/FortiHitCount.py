#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import csv
from netmiko import ConnectHandler
from forticonf import fortigate

## used regardless of choice; used in gen_commands(), is_disabled(), and get_count()
# generates list of policies

def get_policies():
    policy_string = net_connect.send_command('show firewall policy | grep edit')
    #print('a') ##
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
    print('[!] Clearing hit counts ...')
    for command in gen_commands():
        print('') ##
        #net_connect.send_command(command)
    return 0


## used if choice == "show"; used in clean_list()
# generates messy list from output of show commands; used in clean_list()

def messy_list():
    messy_list = []
    for command in gen_commands():
        #print('b') ##
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


## used if choice == "show"; used in get_count()
# generates dictionary of policies and disabled statuses

def is_disabled():
    print('[*] Determining which policies are disabled ...')
    disabled_dict = dict.fromkeys(get_policies())
    for policy_key in disabled_dict:
        #print('c') ##
        if net_connect.send_command('show firewall policy ' + str(policy_key) + ' | grep "set status disable"') != '':
            disabled_dict[policy_key] = 'disabled'
        else:
            disabled_dict[policy_key] = 'enabled'
    return disabled_dict


## used if choice == "show"
# combines the keys (policy ids) with the hit counts (for each policy) into a dictionary

def get_count():
    print('[!] Generating dictionary ...')
    keys = get_policies()
    values = clean_list()
    hit_counts = dict(zip(keys, values))
    disabled_dict = is_disabled()
    for policy_key in disabled_dict:
        if disabled_dict[policy_key] == 'disabled':
            hit_counts[policy_key] = 'disabled'
    return hit_counts


## used if cohice == "show"
# writes hit_counts dictionary into csv file called hit_counts.csv

def write_csv():
    hit_counts = get_count()
    with open('hit_counts.csv', 'w') as f:
        for key in hit_counts.keys():
            f.write("%s,%s\n"%(key,hit_counts[key]))


# logic to determine which commands should be generated/sent

choice = sys.argv[1]

if choice == 'clear':
    base_command = 'di firewall iprope clear 100004'
elif choice == 'show':
    base_command = 'di firewall iprope show 100004'
else:
    sys.exit(1)

print('[*] Using base command: ' + base_command)

print('[*] Connecting ...')
net_connect = ConnectHandler(**fortigate)
print('[+] Successfully connected.')

if choice == 'clear':
    clear_count()
else:
    write_csv()

print('[*] Disconnecting ...')
net_connect.disconnect()
print('[+] Success!')

sys.exit(0)
