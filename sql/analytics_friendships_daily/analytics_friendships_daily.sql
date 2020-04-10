REPLACE INTO `{db_name}`.`{table_name}`

SELECT
                CURRENT_DATE AS datestr,
                COUNT(DISTINCT f.id) AS friendships_active,
                COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) = CURRENT_DATE() THEN id
                        ELSE NULL
					END
				) AS friendships_created,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 1 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_1d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 7 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_7d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 14 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_14d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 30 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_30d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 60 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_60d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 90 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_90d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= CURRENT_DATE - INTERVAL 180 DAY THEN id
                        ELSE NULL
					END
				) AS friendships_created_180d,

				COUNT(DISTINCT
					CASE
						WHEN DATE(f.create_date) >= DATE_TRUNC('month', CURRENT_DATE) THEN id
                        ELSE NULL
					END
				) AS friendships_created_cur_month,

				CURRENT_TIMESTAMP AS _loaded_at

FROM            {db_name}.friendship f

WHERE			1=1
AND				f.status = 'NORMAL'
AND 			f.reply_status = 'ACCEPTED'

GROUP BY        1