-- CREATE TEMPORARY TABLE bm
SELECT 
	b.*,
	m.author, m.title, m.genre2, m.genre3, m.published_date, m.all_genres
FROM best_sellers AS b
LEFT JOIN metadata AS m
	ON b.volumeid = m.volumeid;
--     
-- DROP TEMPORARY TABLE bm;
--     