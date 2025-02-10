WITH temp AS (
SELECT 
	YEAR(b.date_on_list) AS year_,
    m.genre2,
    COUNT(*) AS num_books,
    RANK() OVER(
		PARTITION BY YEAR(b.date_on_list)
        ORDER BY COUNT(*) DESC
    ) r
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid
GROUP BY year_, m.genre2
ORDER BY year_  DESC, COUNT(*) DESC
)
-- SELECT *
-- FROM temp
SELECT 
	year_,
    genre2,
    num_books
FROM temp
WHERE r < 2