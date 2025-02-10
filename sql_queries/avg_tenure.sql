
-- DROP TABLE avg_tenure;
CREATE TABLE avg_tenure AS
-- counts number of times a book was on a bestsellers list for each year
WITH count_entries AS (
SELECT 
	b.volumeid,
	m.title,
    m.author,
    m.genre2,
    YEAR(b.date_on_list) AS year_,
    COUNT(*) OVER(
		PARTITION BY volumeid, YEAR(b.date_on_list)
    ) AS num_times
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid
WHERE m.volumeid IS NOT NULL AND m.volumeid != ''
),

temp AS (
SELECT DISTINCT *
FROM count_entries
)
-- calculate the avg tenure by year and genre
SELECT DISTINCT
	year_,
	genre2,
	AVG(num_times) OVER(
		PARTITION BY year_, genre2
    ) AS avg_time
FROM temp
ORDER BY year_ DESC, avg_time DESC
