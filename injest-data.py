#!/usr/bin/env python3
# This script injests the `ssh-map.json` files from multiple machines in order
# to build a SQLite database of the nodes on the ssh key map.
# SQL help from: https://www.sqlitetutorial.net/sqlite-python

import os
import sys
import json
import getopt
from utils import check_for_file, create_connection, create_table,\
create_row, select_all_rows, delete_row, delete_all_rows

# Function Args.
# check_for_file(filename):
# create_connection(db_file):
# create_table(conn, create_table_sql):
# select_all_rows(conn):
# delete_row(conn, id):
# delete_all_rows(conn):

# Class to hold optional arguments.
class Options:
    def __init__(self):
        self.input_file = "ssh-map.json"

def print_help():
    print("""
    Usage:

           injest-data.py [options]

     -h                    print this help menu
     -f <file_name>        json file to import from, defaults to `ssh-map.json`
    """)

def main():
    # Create DB connection.
    conn = create_connection(r"ssh-map.db")

    # Collection options.
    options = Options()

    # Tj's getopts handling.
    try:
        opts, args_garbage = getopt.getopt(sys.argv[1:], "hf:")
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        print_help()
        exit(2)

    if args_garbage:
        print("\nContains cmd line garbage:" + str(args_garbage) + "\n")
        print_help()
        exit(5)

    for opt, arg in opts:
        if opt == "-h":
            print_help()
            exit(1)
        elif opt == "-f":
            options.input_file = arg


    # Create table SQL.
    create_table_sql = """CREATE TABLE IF NOT EXISTS ssh_map (
        lhost text NOT NULL,
        lhost_pub_ip text NOT NULL,
        rhost text NOT NULL,
        users text NOT NULL,
        PRIMARY KEY (lhost, rhost)
    );
    """

    # Check SQL connection obj and creates ssh_map table.
    if conn is not None:
        # Create ssh_map table.
        create_table(conn, create_table_sql)

    # Read in contents of ssh-map.json.
    data_file_name = "ssh-map.json"
    check_for_file(data_file_name)
    ssh_json_file = open(data_file_name, 'r')
    json_data = json.load(ssh_json_file)
    ssh_json_file.close()

    # Get's initial number of rows in ssh_map table.
    initial_db_rows = select_all_rows(conn)
    
    for obj in json_data:
        values = (obj['lhostname'], obj['lhost_pub_ip'], obj['rhostname'],
                str(obj['users']))
        # Slap data into DB.
        create_row(conn, values)

    # Check if num rows in ssh_map table has changed, aka if the above json
    # file was imported.
    db_rows = select_all_rows(conn)
    if initial_db_rows < db_rows:
        print("Data Entered in DB!")
    elif initial_db_rows == db_rows:
        print("No Data Entered into DB!")
        print("Perhaps you're trying to import duplicate json?")

if __name__ == '__main__':
    main()
