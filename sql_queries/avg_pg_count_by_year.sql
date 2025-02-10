SELECT 
	DISTINCT YEAR(b.date_on_list) AS year_,
    AVG(m.pg_count) OVER(
		PARTITION BY YEAR(b.date_on_list)
    ) AS avg_pg_count
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid