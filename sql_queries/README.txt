This folder contains the SQL scripts:

- db_queries.sql: Database schema creation script using PostgreSQL console.
- sum_query.sql: Script that returns transactions for the users 345 and 1234, aggregated monthly, sorted by month, 
				 for the period from 15.02.2020 till 06.06.2020.
- PostgreSQL_database_dump.sql: Script of database schema creation using pgAdmin4. 
								Command: pg_dump -U username -h localhost -s databasename >> PostgreSQL_database_dump.sql