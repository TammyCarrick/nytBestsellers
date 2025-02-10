CREATE TABLE best_sellers AS
SELECT 
	v.volumeid,
    r.date_on_list,
    r.rank_,
    r.prev_rank,
    num_weeks,
    r.publisher AS publisher_nyt,
    r.type_
FROM raw_data AS r
LEFT JOIN volumeid AS v
	ON r.author = v.author AND r.title = v.title
ORDER BY r.author, r.title;
 
 
-- DROP TABLE best_sellers;