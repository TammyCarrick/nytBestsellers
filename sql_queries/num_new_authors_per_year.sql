-- CREATE TABLE num_new_authors AS 
-- list of authors with a ranking of their titles in ASC order of when the title appeared on the nyt best seller list
WITH temp AS (
SELECT  DISTINCT
	author,
    title,
    YEAR(date_on_list) AS year_,
    RANK() OVER(
		PARTITION BY author
        ORDER BY date_on_list ASC
    ) AS r
FROM bm
WHERE author IS NOT NULL
),
-- only select the very first appearance date
first_year AS (
SELECT DISTINCT 
	author,
    year_
FROM temp
WHERE r = 1
),
-- count number of authors in each year
temp2 AS (
SELECT 
	year_,
    COUNT(*) AS num_new_authors
FROM first_year
GROUP BY year_
)
SELECT *
FROM temp2
ORDER BY year_