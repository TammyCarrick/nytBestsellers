CREATE TEMPORARY TABLE to_swap AS 
-- volumes where genre2 = 'General' and genre3 not null; 
SELECT DISTINCT
	volumeid, 
    title,
    genre2,
    genre3,
    all_genres
FROM bm
WHERE genre2 = 'General' AND genre3 !='';

-- ALTER TABLE metadata
-- ADD COLUMN temp_ VARCHAR(100);

UPDATE metadata
SET temp_ = genre2, genre2= genre3
WHERE volumeid IN (SELECT volumeid FROM to_swap);

UPDATE metadata
SET genre3 = temp_
WHERE temp_='General';

ALTER TABLE metadata
DROP COLUMN temp_;
