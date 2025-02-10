CREATE TEMPORARY TABLE  temp_dupes AS
SELECT volumeid
FROM nyt_best_sellers.volumeid
GROUP BY volumeid
HAVING COUNT(*)>1;

DELETE FROM volumeid
WHERE volumeid IN (SELECT volumeid FROM temp_dupes);

DROP TABLE temp_dupes