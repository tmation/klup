REPLACE INTO `{db_name}`.`{table_name}`

SELECT
                DATE('{DATE}') AS datestr,
                COUNT(DISTINCT f.id) AS friendships_active,
                COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) = DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 1 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_1d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 7 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_7d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 14 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_14d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 30 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_30d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 60 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_60d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 90 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_90d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.update_date) BETWEEN DATE('{DATE}') - INTERVAL 180 DAY AND DATE('{DATE}') THEN id
                        ELSE NULL
					END
				) AS friendships_created_180d,

				COUNT(DISTINCT
					CASE
						WHEN DATE_TRUNC('month', DATE(f.update_date)) = DATE_TRUNC('month', DATE('{DATE}')) THEN id
                        ELSE NULL
					END
				) AS friendships_created_cur_month,

				CURRENT_TIMESTAMP AS _loaded_at

FROM            {db_name}.friendship f

WHERE			1=1
AND				f.status = 'NORMAL'
AND 			f.reply_status = 'ACCEPTED'

GROUP BY        1