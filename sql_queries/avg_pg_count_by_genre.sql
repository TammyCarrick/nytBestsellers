-- SELECT DISTINCT genre2, 
-- 	AVG(pg_count)OVER(
-- 		PARTITION BY genre2
--     ) AS avg_pg_count,
--     COUNT(*) OVER(
-- 		PARTITION BY genre2
--     ) AS num_books
-- FROM metadata
-- ORDER BY num_books DESC
-- 	

SELECT 
	DISTINCT YEAR(b.date_on_list) AS year_, 
    m.genre2,
    COUNT( *) OVER(
		PARTITION BY m.genre2
    ) AS num_entries
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid
WHERE genre2 IS NOT NULL AND genre2 != '' AND YEAR(b.date_on_list) = '2017'
ORDER BY year_ DESC,  num_books DESC
