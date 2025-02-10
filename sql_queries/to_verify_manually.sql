-- in the volume_id table and not the verified_id table
SELECT vol.volumeid, vol.title, vol.title_rslt, vol.author, vol.last_name
FROM volumeid AS vol
LEFT JOIN verified_ids AS ver
	ON vol.volumeid = ver.volumeID
WHERE ver.volumeID IS NULL
ORDER BY last_name;

-- deleting unverifiable results
CREATE TEMPORARY TABLE remove_vol AS
SELECT vol.volumeid, vol.title, vol.title_rslt, vol.author, vol.last_name
FROM volumeid AS vol
LEFT JOIN verified_ids AS ver
	ON vol.volumeid = ver.volumeID
WHERE ver.volumeID IS NULL;

DELETE FROM volumeid
WHERE volumeid IN (SELECT volumeid FROM remove_vol);

DROP TABLE remove_vol;

