SELECT ver.volumeid
FROM verified_ids AS ver
	LEFT JOIN metadata AS met
		ON ver.volumeid = met.volumeid
WHERE met.volumeid IS NULL