SELECT 
	volumeid,
    author,
    title,
    published_date,
    isbn10
FROM metadata
WHERE CHAR_LENGTH(published_date) < 10