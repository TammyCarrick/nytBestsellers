-- count number of books by year, author and genre
-- CREATE TABLE  most_prolific_author AS
WITH temp AS (
SELECT 
	YEAR(b.date_on_list) AS year_,
    m.author,
    m.genre2,
    COUNT(*)  AS num_entries
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid
GROUP BY year_, author, genre2
-- ORDER BY year_ DESC, genre2 DESC, COUNT(*) DESC
),
temp2 AS (
SELECT *,
	RANK() OVER(
		PARTITION BY year_, genre2
        ORDER BY num_entries DESC
    ) AS r
FROM temp
)
SELECT *
FROM temp2
WHERE r =1 AND genre2 IS NOT NULL
ORDER BY year_ DESC, num_entries DESC