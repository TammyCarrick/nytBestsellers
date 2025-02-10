SELECT
	YEAR(date_on_list) AS year_,
    MONTH(date_on_list)AS month_,
    COUNT(*)
FROM bm
WHERE YEAR(date_on_list) = '2022'
GROUP BY year_, month_
ORDER BY year_ DESC, month_