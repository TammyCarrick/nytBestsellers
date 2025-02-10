-- each books longest tenure
CREATE TABLE longest_tenured_books AS 

-- counts number of times a book was on a bestsellers list for each year
WITH count_entries AS (
SELECT 
	b.volumeid,
	m.title,
    m.author,
    m.genre2,
    b.num_weeks,
    YEAR(b.date_on_list) AS year_,
    COUNT(*) OVER(
		PARTITION BY volumeid, YEAR(b.date_on_list)
    ) AS num_times
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid
WHERE m.volumeid IS NOT NULL AND m.volumeid != ''
),
genre_rank AS(
	SELECT *,
    RANK() OVER(
		PARTITION BY year_, genre2
        ORDER BY num_times DESC, num_weeks DESC, author 
    ) AS r
    FROM count_entries
)
SELECT DISTINCT *
FROM genre_rank
WHERE r = 1 -- AND year_ = '2023'
ORDER BY year_,  num_times DESC;

-- DROP TABLE longest_tenured_books;