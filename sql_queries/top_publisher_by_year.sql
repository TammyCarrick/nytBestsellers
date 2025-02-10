WITH temp AS (
SELECT 
	YEAR(Date_on_list) AS year_,
	publisher,
	COUNT(*) AS c
FROM raw_data
GROUP BY publisher, year_
ORDER BY year_ DESC , COUNT(*) DESC
),
temp2 AS (
	SELECT *,
		RANK() OVER(
			PARTITION BY year_
            ORDER BY c DESC
        ) AS r
	FROM temp
)
SELECT *
FROM temp2
WHERE r < 4
ORDER BY year_ DESC