# BI_Practical_assignment

This program creates connection and execute SQL insert queries on PostgreSQL database after reading data from CSV files and executing the necessary data preparation steps for malformed data.
The data preparation steps are:
Check dataframes information: get types of elements and look for null values.
Filter out those rows which does not contain any data.
Look for duplicated ID: duplicated ID will raise an error when populating database.
Change dataframes columns types to harmonize with database schema.
Replace single quote in strings with double quote (single quote error when inserting values into tables).
Convert date columns to a well defined format that can be parsed by database.

This program is tested on Windows OS, Python 3.7

The Python modules needed are:
pandas
pathlib
os
psycopg2
datetime
re
dateutil.parser

For database creation, install PostgreSQL on your machine and you can use pgAdmin or PostgreSQL console to create database schema.
Database is composed of two enumerated types valid_transaction_type and valid_account_type with three tables persons, accounts and transactions.

The sql_queries folder contains the SQL scripts:
- db_queries.sql: Database schema creation script using PostgreSQL console.
- sum_query.sql: Script that returns transactions for the users 345 and 1234, aggregated monthly, sorted by month, 
				 for the period from 15.02.2020 till 06.06.2020.
- PostgreSQL_database_dump.sql: Script of database schema creation using pgAdmin4. 
								Command: pg_dump -U username -h localhost -s databasename >> PostgreSQL_database_dump.sql
                
The data folder contains CSV files:
- List of customers with their personal data: BI_assignment_person.csv
- List of accounts that belong to the customers: BI_assignment_account.csv
- List of transactions from/to these accounts: BI_assignment_transaction.csv
