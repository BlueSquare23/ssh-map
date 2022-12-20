#!/usr/bin/env python3
# This script helps enumerate ssh key networks. It does so by trying to log
# into each of the hosts in the `ssh-hosts.txt` file as each of the users in
# the `ssh-users.txt` file.
# Written by, John R., Dec. 2022

import os
import sys
import socket
import requests
import json
import time
import getopt
from utils import check_for_file
from paramiko import SSHClient, MissingHostKeyPolicy

# Remote SSH Host Class.
class SshHost:
    def __init__(self):
        self.lhostname = ""
        self.rhostname = ""
        self.lhost_pub_ip = ""
        self.ssh_port = 22
        self.users = []

    def __str__(self):
        str_repr = "###### SSH Host Object ###### \n"
        str_repr += "Local Host: " + self.lhostname + "\n"
        str_repr += "Remote Host: " + self.rhostname + "\n"
        str_repr += "Local Public IP: " + self.lhost_pub_ip + "\n"
        str_repr += "SSH Port: " + str(self.ssh_port) + "\n"
        str_repr += "Valid Users(s): " + str(self.users) + "\n"
        return str_repr

# Make SshHost class JSON serializable.
class SshHostEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

# Class to hold optional arguments.
class Options:
    def __init__(self):
        self.pretty_print = ""
        self.raw = ""
        self.output_file = "ssh-map.json"
        self.delay = .5

def print_help():
    print("""
    Usage:

           ssh-mapper.py [options]

     -h                    print this help menu
     -p                    print output plain text
     -r                    print output as raw json (mutes ticker)
     -o <file_name>        write to file, defaults to `ssh-map.json`
     -d <delay>            delay seconds between ssh attempts
    """)

def main():

    options = Options()

    try:
        opts, args_rubbish = getopt.getopt(sys.argv[1:], "hpro:d:")
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        print_help()
        exit(2)

    if args_rubbish:
        print("\nContains cmd line garbage:" + str(args_garbage) + "\n")
        print_help()
        exit(5)

    for opt, arg in opts:
        if opt == "-h":
            print_help()
            exit(1)
        elif opt == "-p":
            options.pretty_print = "yes"
        elif opt == "-r":
            options.raw = "yes"
        elif opt == "-o":
            options.output_file = arg
        elif opt == "-d":
            try:
                options.delay = int(arg)
            except ValueError:
                print("Integers Only!")
                print_help()
                exit(9)

    # Amount of time b/w ssh connection attempts.
    delay_time = options.delay

    hosts_and_ports = {}

    # Read in contents of ssh-hosts.txt.
    host_file_name = "ssh-hosts.txt"
    check_for_file(host_file_name)

    ssh_hosts_file = open(host_file_name, 'r')
    while True:
        # Get next line from file.
        line = ssh_hosts_file.readline()
        line = line.rstrip("\n")

        # If line is empty end of file is reached.
        if not line:
            break

        # Gather host and port info.
        rhost = line.split(":")[0]
        rport = line.split(":")[1]
        hosts_and_ports[rhost] = rport

    ssh_hosts_file.close()

    # Read in contents of ssh-users.txt.
    users_file_name = "ssh-users.txt"
    check_for_file(users_file_name)

    potential_users = []

    ssh_users_file = open(users_file_name, 'r')
    while True:
        # Get next line from file.
        line = ssh_users_file.readline()
        line = line.rstrip("\n")

        # If line is empty end of file is reached.
        if not line:
            break

        potential_users.append(line)

    ssh_users_file.close()

    # Get WAN IP using ipinfo.io API.
    r = requests.get("https://ipinfo.io/")
    lhost_pub_ip = json.loads(r.text)['ip']

    all_ssh_host_objs = []

    lhost = os.uname()[1]

    # Don't output ticker in raw json mode.
    if options.raw != "yes":
        print("Trying SSH Connections...", end="", flush=True)

    for host in hosts_and_ports:
        client = SSHClient()
        client.set_missing_host_key_policy(MissingHostKeyPolicy())

        new_host = SshHost()
        new_host.lhostname = lhost
        new_host.rhostname = host

        new_host.lhost_pub_ip = lhost_pub_ip
        new_host.ssh_port = int(hosts_and_ports[host])

        valid_users = []

        for user in potential_users:
            if options.raw != "yes":
                print(".", end="", flush=True)

            time.sleep(delay_time)
            try:
                client.connect(new_host.rhostname, port=new_host.ssh_port,
                    username=user, look_for_keys=True)
                valid_users.append(user)
            except Exception as e:
                pass

        new_host.users = valid_users

        all_ssh_host_objs.append(new_host)

        client.close()

    if options.raw != "yes":
        print(".", flush=True)

    # Is place for data.
    data = []

    for host_obj in all_ssh_host_objs:
        if len(host_obj.users) > 0:
            if options.pretty_print == "yes":
                print(host_obj)

            data.append(host_obj)

    # Write json output to options.output_file.
    f = open(options.output_file, "w")
    json_data = json.dumps(data, indent=4, cls=SshHostEncoder)
    f.write(json_data)
    f.close()

    if options.raw == "yes":
        print(json_data)
    else:
        print("Results written to: " + options.output_file)

if __name__ == '__main__':
    main()
