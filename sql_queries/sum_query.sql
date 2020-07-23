/* A query that returns transactions for the users 345 and 1234, aggregated monthly, sorted
by month, for the period from 15.02.2020 till 06.06.2020*/

SELECT id_person, to_char(transaction_date, 'MM.YYYY') AS month, sum(transaction_amount) as sum_of_transactions
FROM transactions, accounts 
WHERE accounts.id = transactions.id_account 
	AND accounts.id_person in (345,1234)
	AND transaction_date >= '2020-02-15'
	AND transaction_date <=  '2020-06-06'
GROUP BY id_person, month
ORDER BY id_person DESC
