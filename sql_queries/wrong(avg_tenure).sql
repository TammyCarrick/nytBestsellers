-- CREATE TABLE avg_tenure

WITH temp AS (
	SELECT 
		b.volumeid,
		b.num_weeks,
        YEAR(b.date_on_list) AS year_,
		RANK() OVER(
			PARTITION BY b.volumeid
			ORDER BY b.date_on_list DESC
		) AS r,
        m.genre2
	FROM best_sellers AS b
		RIGHT JOIN metadata AS m
			ON b.volumeid = m.volumeid
-- 	WHERE volumeid IS NOT NULL
),
max_weeks AS (
	SELECT 
		volumeid,
        num_weeks,
        year_,
        genre2
	FROM temp
    WHERE r = 1
)
-- avg num of weeks on nyt best sellers
-- SELECT 
-- 	AVG(num_weeks)
-- FROM max_weeks

-- avg num of weeks on nyt best sellers list by genre
SELECT 
    DISTINCT genre2,
    year_,
    AVG(num_weeks) OVER(
		PARTITION BY genre2
    ) AS avg_num_weeks,
    COUNT(*) OVER(
		PARTITION BY genre2
    ) AS num_books
FROM max_weeks
WHERE year_ = '2024'
ORDER BY avg_num_weeks DESC;

-- DROP TABLE avg_tenure;