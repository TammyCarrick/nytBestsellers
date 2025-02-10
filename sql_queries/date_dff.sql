WITH temp AS (
	SELECT 
		m.published_date,
        b.date_on_list,
		m.genre2,
		m.author,
        m.title,
		RANK() OVER (
			PARTITION BY m.volumeid
			ORDER BY b.date_on_list ASC
		) AS r
	FROM metadata AS m
	LEFT JOIN best_sellers AS b
		ON m.volumeid = b.volumeid
	WHERE CHAR_LENGTH(m.published_date) = 10

  ),

  first_date AS (
	SELECT *
    FROM temp
    WHERE r = 1
  )
  
SELECT  *,
	 DATEDIFF(date_on_list, published_date) AS date_diff
FROM first_date
ORDER BY date_diff
