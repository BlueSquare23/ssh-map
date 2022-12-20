#!/usr/bin/env python3
# A collection of utilities / helper functions for the other scripts.
# SQL help from: https://www.sqlitetutorial.net/sqlite-python
# Written by, John R., Dec. 2022

import os
import sqlite3
from sqlite3 import Error

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

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_row(conn, values):
    """
    Create a new row in the ssh_map table
    Rows have compound keys lhost,rhost
    :param conn: The Connection object
    :param values: The ssh obj values
    :return: row id
    """
    sql = ''' INSERT OR IGNORE INTO ssh_map(lhost,lhost_pub_ip,rhost,users)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid

def select_all_rows(conn):
    """
    Query all rows in the ssh_map table
    :param conn: The Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT * FROM ssh_map'
    cur.execute(sql)

    rows = cur.fetchall()
    return len(rows)

#    for row in rows:
#        ssh_map_id = row[0]
#        user = row[1]
#        ssh_map = row[2]
#        ssh_map = f"{ssh_map}"
#        print(ssh_map)

def delete_row(conn, id):
    """
    Delete a ssh_map by id
    :param conn: Connection to the SQLite database
    :param id: Compound key of the ssh_map entry
    :return:
    """
    sql = 'DELETE FROM ssh_map WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_all_rows(conn):
    """
    Delete all rows in the ssh_map table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM ssh_map'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

