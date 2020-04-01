REPLACE INTO `{db_name}`.`{table_name}`

SELECT
				CURRENT_DATE() AS datestr,
                COUNT(DISTINCT f.id) AS friendships_active,
                COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) = CURRENT_DATE() THEN id
                        ELSE NULL
					END
				) AS friendships_created

FROM 			friendship f

WHERE 			f.status = 'NORMAL'

GROUP BY		1