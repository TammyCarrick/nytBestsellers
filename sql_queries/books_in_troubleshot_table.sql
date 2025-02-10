--  books in the raw_data table that aren't in the volumeid table; these should be in troubleshoot_id table
WITH entries AS (
SELECT DISTINCT r.author, r.title 
FROM raw_data AS r
LEFT JOIN volumeid AS v
	ON r.title = v.title
WHERE v.title IS NULL
ORDER BY author DESC, title DESC
)
SELECT *
FROM entries

