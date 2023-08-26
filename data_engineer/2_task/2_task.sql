-- Создание таблиц
CREATE TABLE Sales
(
    contact_id BIGINT NOT NULL,
    contact_date TIMESTAMP NOT NULL,
    sell_date TIMESTAMP,
    sell_amt NUMERIC,
    contact_type VARCHAR(255) NOT NULL,
    filial VARCHAR(255) NOT NULL,
    manager VARCHAR(255) NOT NULL
);


-- Первый запрос
SELECT month, year,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sum_sales) AS median_sales
FROM (
SELECT
  EXTRACT(month FROM sell_date) AS month,
  EXTRACT(year FROM sell_date) AS year,
  manager,
  SUM(sell_amt) AS sum_sales
FROM public.sales
GROUP BY year, month, manager
HAVING SUM(sell_amt) > 0
	) sub
GROUP BY year, month
ORDER BY year, month



-- Второй запрос
WITH count_between_contacts AS (
SELECT
	manager,
	DATE_TRUNC('Day', contact_date) AS contact_date,
	EXTRACT(day FROM (contact_date - LAG(contact_date) OVER (PARTITION BY manager ORDER BY contact_date))) AS dbc
FROM public.sales
WHERE sell_date IS NOT NULL
),

days_between_contacts AS (
SELECT manager, contact_date, MAX(dbc) AS dbc
FROM count_between_contacts
GROUP BY manager, contact_date
ORDER BY manager, contact_date
),

counter AS (
  SELECT
 	* ,
 	ROW_NUMBER() OVER (PARTITION BY manager ORDER BY contact_date ASC) -
 	ROW_NUMBER() OVER (PARTITION BY manager, dbc ORDER BY contact_date ASC) AS gr
  from days_between_contacts
)

SELECT
  	manager, dbc, COUNT(*) AS counts
FROM counter
GROUP BY manager, dbc, gr
ORDER BY counts DESC
LIMIT 1;