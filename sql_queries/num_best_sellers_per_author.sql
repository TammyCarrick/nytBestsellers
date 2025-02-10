SELECT author, COUNT(*)
FROM nyt_best_sellers.metadata
GROUP BY author
ORDER BY COUNT(*) DESC;