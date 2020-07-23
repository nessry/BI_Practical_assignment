/*Create transaction_db database*/
CREATE DATABASE transaction_db
    WITH 
    OWNER = postgres

COMMENT ON DATABASE transaction_db
    IS 'Database that contains:
• List of customers with their personal data
• List of accounts that belong to the customers
• List of transactions from/to these accounts';

/*Create enumerated type valid_account_type to insert account types*/
CREATE TYPE valid_account_type AS ENUM
    ();

/*Create enumerated type valid_transaction_type to insert transaction types*/
CREATE TYPE valid_transaction_type AS ENUM
    ();
	
/*Create persons table to insert list of customers with their personal data*/
CREATE TABLE persons
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50),
    zip VARCHAR(10) NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT,
    birth_date date NOT NULL,
);

/*Create accounts table to insert list of accounts that belong to the customers*/
CREATE TABLE accounts
(
    id SERIAL PRIMARY KEY,
    id_person bigint NOT NULL,
    account_type valid_account_type NOT NULL,
	FOREIGN KEY (id_person)
      REFERENCES persons(id),
);

/*Create transactions table to insert list of transactions from/to the accounts*/
CREATE TABLE transactions
(
    id SERIAL PRIMARY KEY,
    id_account bigint NOT NULL,
    transaction_type valid_transaction_type NOT NULL,
    transaction_date date NOT NULL,
    transaction_amount numeric NOT NULL,
    FOREIGN KEY (id_account)
      REFERENCES accounts(id),
);

