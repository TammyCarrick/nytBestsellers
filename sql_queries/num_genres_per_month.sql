SELECT
	YEAR(date_on_list) AS year_,
	MONTH(date_on_list) AS month_,
    genre2,
    COUNT(*) 
FROM bm
WHERE genre2 IS NOT NULL AND genre2 != '' AND YEAR(date_on_list) = '2022'
GROUP BY year_, month_, genre2
ORDER BY  year_ DESC, month_, COUNT(*) DESC

