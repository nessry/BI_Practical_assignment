# -*- coding: utf-8 -*-
"""
@author: Nessrine Hammami

This file contains the functions to create connection and execute Python SQL queries on PostgreSQL database
"""

import psycopg2 # Python SQL module to interact with PostgreSQL
from psycopg2 import OperationalError

# Function to create connection to a PostgreSQL database using database credentials
def create_connection(db_config):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port'],
        )
        print("Connection to PostgreSQL DB: successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to execute Python SQL queries on PostgreSQL database
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")