CREATE TABLE raw_data_searchable  AS (
WITH ranked AS (
	SELECT 
		author,
		title,
		date_on_list,
		RANK() OVER(
			PARTITION BY author, title
			ORDER BY date_on_list
		) AS date_order
	FROM raw_data
)
SELECT author, title, date_on_list
FROM ranked
WHERE date_order = 1
)