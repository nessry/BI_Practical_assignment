# -*- coding: utf-8 -*-
"""
@author: Nessrine Hammami

This file contains functions for data preparation and execution of insert SQL queries on PostgreSQL database
"""

import pandas as pd
from pathlib import Path
import os

from db_credentials import postgresql_db_config 
from db_connection import create_connection, execute_query
from date_process import convert_date_treatment

# csv files directory
data_dir = Path(__file__).absolute().parents[0] / 'data'

# Function to read csv files into dataframes
def read_data(file_name):
    full_path = os.path.join(str(data_dir), file_name)
    df = pd.read_csv(full_path, low_memory=False)
    return df

# Function to prepare data
def prepare_date():
    print('---Import data from CSV files---')
    account_df = read_data("BI_assignment_account.csv")
    person_df = read_data("BI_assignment_person.csv")
    transaction_df = read_data("BI_assignment_transaction.csv")
    
    # First step: check dataframes information: get types of elements and look for null values
    print('---First step: check dataframes information: get types of elements and look for null values---')
    
    print(person_df.info())
    print(account_df.info())
    print(transaction_df.info())
    
    print(person_df.dtypes)
    print(account_df.dtypes)
    print(transaction_df.dtypes)
    
    print(person_df.isnull())
    print(account_df.isnull())
    print(transaction_df.isnull())
    
    # Second step: filter out those rows which does not contain any data 
    print('---Second step: Drop empty rows---')
    
    person_df = person_df.dropna(how = 'all') 
    transaction_df = transaction_df.dropna(how = 'all') 
    account_df = account_df.dropna(how = 'all') 
    
    # Third Step: Look for duplicated ID: duplicated ID will raise an error when populating database
    print('---Third Step: Look for duplicated IDs and replace them---')
    
    duplicate_person_id = person_df[person_df.duplicated(['id_person'])]
    duplicate_account_id = account_df[account_df.duplicated(['id_account'])]
    duplicate_transaction_id = transaction_df[transaction_df.duplicated(['id_transaction'])]
    print(duplicate_person_id)
    print(duplicate_account_id)
    print(duplicate_transaction_id)
    # Based on printed results, transaction_df contains duplicated ID (2439) for 115 rows
    for index, row in duplicate_transaction_id.iterrows():
        transaction_df.loc[index,'id_transaction'] = index + 2 # Replace duplicated IDs
        
    # We can also look for duplicated email if we choose to set email as unique
    #duplicate_email = person_df[person_df.duplicated(['email'])]
    #print(duplicate_email)
    
    # Fourth Step: Change dataframes columns types to harmonize with database schema
    print('---Fourth Step: Change dataframes columns types to harmonize with database schema---')
    
    person_df['id_person'] = person_df['id_person'].astype(int)
    person_df['name'] = person_df['name'].astype(str)
    person_df['surname'] = person_df['surname'].astype(str)
    person_df['zip'] = person_df['zip'].astype(int)
    person_df['city'] = person_df['city'].astype(str)
    person_df['country'] = person_df['country'].astype(str)
    person_df['email'] = person_df['email'].astype(str)
    person_df['phone_number'] = person_df['phone_number'].astype(str)
    person_df['birth_date'] = person_df['birth_date'].astype(str)
    
    account_df['id_account'] = account_df['id_account'].astype(int)
    account_df['id_person'] = account_df['id_person'].astype(int)
    account_df['account_type'] = account_df['account_type'].astype(str)
    
    transaction_df['id_transaction'] = transaction_df['id_transaction'].astype(int)
    transaction_df['id_account'] = transaction_df['id_account'].astype(int)
    transaction_df['transaction_type'] = transaction_df['transaction_type'].astype(str)
    transaction_df['transaction_date'] = transaction_df['transaction_date'].astype(str)
    
    # Fifth Step: Replace single quote in strings with double quote (single quote error when inserting values into tables)
    print('---Fifth Step: Replace single quote in strings with double quote---')
    
    person_df = person_df.replace({'\'': '"'}, regex=True)
    account_df = account_df.replace({'\'': '"'}, regex=True)
    transaction_df = transaction_df.replace({'\'': '"'}, regex=True)
    
    # Sixth Step: Convert date columns to a well defined format that can be parsed by database
    print('---Sixth Step: Convert date columns to a well defined format---')
    
    for i in range(person_df.shape[0]):
        person_df.loc[i,'birth_date'] = convert_date_treatment(person_df.loc[i,'birth_date'])
    for j in range(transaction_df.shape[0]):
        transaction_df.loc[j,'transaction_date'] = convert_date_treatment(transaction_df.loc[j,'transaction_date'])
    
    return account_df, person_df, transaction_df

# Function to get the different categories of account_type and transaction_type
def get_type_categories(df,col):
    types = df[col].unique()
    return types

def main():
  account_df, person_df, transaction_df = prepare_date()
  account_types = get_type_categories(account_df,'account_type')
  print("The different account types are:")
  print(account_types)
  transaction_types = get_type_categories(transaction_df,'transaction_type')
  print("The different transaction types are:")
  print(transaction_types)
  
  # Establish connection
  print('---Trying to connect to Database---')
  connection = create_connection(postgresql_db_config)
  
  # Populate Enumerated type valid_account_type in database with different account types values
  for val in account_types:
      valid_account_type_insert = "ALTER TYPE valid_account_type ADD VALUE " + "'" + str(val) + "';"
      execute_query(connection, valid_account_type_insert)
  # Populate Enumerated type valid_transaction_type in database with different transaction types values
  for val in transaction_types:
      valid_transaction_type_insert = "ALTER TYPE valid_transaction_type ADD VALUE " + "'" + str(val) + "';"
      execute_query(connection, valid_transaction_type_insert)
      
  # Insert customers information into persons table of database
  for index, row in person_df.iterrows():
      customers_records_insert="INSERT INTO persons (id,name,surname,zip,city,country,email,phone_number,birth_date) VALUES " + str(tuple(row.values)) +";"
      execute_query(connection, customers_records_insert)
      
  # Insert accounts information into accounts table of database
  for index, row in account_df.iterrows():
      accounts_records_insert="INSERT INTO accounts (id,id_person,account_type) VALUES " + str(tuple(row.values)) +";"
      execute_query(connection, accounts_records_insert)
  
  # Insert transactions information into transactions table of database
  for index, row in transaction_df.iterrows():
      transactions_records_insert="INSERT INTO transactions (id,id_account,transaction_type, transaction_date, transaction_amount) VALUES " + str(tuple(row.values)) +";"
      execute_query(connection, transactions_records_insert)
  
  connection.commit()
  connection.close()
  
if __name__ == "__main__":
  main()