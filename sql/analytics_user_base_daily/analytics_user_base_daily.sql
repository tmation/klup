REPLACE INTO `{db_name}`.`{table_name}`

SELECT
                CURRENT_DATE AS datestr,
                COUNT(DISTINCT CASE WHEN last_active_date < CURRENT_DATE() - INTERVAL 180 DAY THEN klupper_id ELSE NULL END) AS dormant_users,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 1 DAY THEN klupper_id ELSE NULL END) AS active_1d,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 7 DAY THEN klupper_id ELSE NULL END) AS active_7d,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 14 DAY THEN klupper_id ELSE NULL END) AS active_14d,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 30 DAY THEN klupper_id ELSE NULL END) AS active_30d,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 60 DAY THEN klupper_id ELSE NULL END) AS active_60d,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 90 DAY THEN klupper_id ELSE NULL END) AS active_90d,
                COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 180 DAY THEN klupper_id ELSE NULL END) AS active_180d,
                COUNT(DISTINCT CASE WHEN last_active_date >= DATE_TRUNC('month', CURRENT_DATE()) THEN klupper_id ELSE NULL END) AS active_cur_month,

                CURRENT_TIMESTAMP AS _loaded_at

FROM            {db_name}.klupper_last_active_date
