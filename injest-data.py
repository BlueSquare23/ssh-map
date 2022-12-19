#!/usr/bin/env python3
# This script injests the `ssh-map.json` files from multiple machines in order
# to build a SQLite database of the nodes on the ssh key map.
# SQL help from: https://www.sqlitetutorial.net/sqlite-python

import os
import sys
import json
from utils import check_for_file, create_connection, create_table,\
create_row, select_all_rows, delete_row, delete_all_rows

# Function Args.
# check_for_file(filename):
# create_connection(db_file):
# create_table(conn, create_table_sql):
# select_all_rows(conn):
# delete_row(conn, id):
# delete_all_rows(conn):

if __name__ == '__main__':
    # Create DB connection.
    conn = create_connection(r"ssh_map.db")

    create_table_sql = """CREATE TABLE IF NOT EXISTS ssh_map (
        id integer PRIMARY KEY,
        lhost text NOT NULL,
        lhost_pub_ip text NOT NULL,
        rhost text NOT NULL,
        users text NOT NULL
    );
    """
    if conn is not None:
        # Create links table.
        create_table(conn, create_table_sql)

    # Read in contents of ssh-map.json.
    data_file_name = "ssh-map.json"
    check_for_file(data_file_name)
    ssh_json_file = open(data_file_name, 'r')
    json_data = json.load(ssh_json_file)
    ssh_json_file.close()
    
    for obj in json_data:
        values = (obj['lhostname'], obj['lhost_pub_ip'], obj['rhostname'], str(obj['users']))
        create_row(conn, values)
        
    print("Data Entered in DB!")
