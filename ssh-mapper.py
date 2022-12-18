#!/usr/bin/env python3
# This script helps ennumerate ssh key networks. It does so by trying to log
# into each of the hosts in the `ssh-hosts.txt` file as each of the users in
# the `ssh-users.txt` file.

import os
import socket
import requests
import json
import time
from paramiko import SSHClient, MissingHostKeyPolicy

# Ammount of time b/w ssh connection attempts.
delay_time = .5

# Remote SSH Host Class.
class SshHost:
    def __init__(self):
        self.lhostname = ""
        self.rhostname = ""
        self.lhost_pub_ip= ""
        self.ssh_port = ""
        self.users = []

    def __str__(self):
        str_repr = "###### SSH Host Obj ###### \n"
        str_repr += "Local Host: " + self.lhostname + "\n"
        str_repr += "Remote Host: " + self.rhostname + "\n"
        str_repr += "SSH Port: " + str(self.ssh_port) + "\n"
        str_repr += "Valid Users(s): " + str(self.users) + "\n"
        return str_repr

# Make SshHost class JSON serializable.
class SshHostEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

# Makes sure file(s) exists and has contents.
def check_for_file(filename):
    try:
        if os.stat(filename).st_size == 0:
            print(f"Empty file: {filename}")
            exit(3)
    except OSError:
        print(f"No file: {filename}")
        exit(4)

    return

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

print("Trying SSH Connections...", end="", flush=True)

for host in hosts_and_ports:
    client = SSHClient()
    client.set_missing_host_key_policy(MissingHostKeyPolicy())

    new_host = SshHost()
    new_host.lhostname = os.uname()[1]
    new_host.rhostname = host

    new_host.lhost_pub_ip = lhost_pub_ip
    new_host.ssh_port = hosts_and_ports[host]

    valid_users = []

    for user in potential_users:
        print(".", end="", flush=True)

        time.sleep(delay_time)
        try:
            client.connect(new_host.rhostname, port=new_host.ssh_port, username=user, look_for_keys=True)
            valid_users.append(user)
        except Exception as e:
            pass

    new_host.users = valid_users

    all_ssh_host_objs.append(new_host)

    client.close()

print(".", flush=True)

for host_obj in all_ssh_host_objs:
    if len(host_obj.users) > 0:
#        print(host_obj)
        host_obj_json = json.dumps(host_obj, indent=4, cls=SshHostEncoder)
        print(host_obj_json)
