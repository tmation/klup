REPLACE INTO `klup_tmation`.`analytics_user_base_daily`

SELECT
				CURRENT_DATE() AS datestr,
				COUNT(DISTINCT CASE WHEN last_active_date < CURRENT_DATE() - INTERVAL 180 DAY THEN id ELSE NULL END) AS dormant_users,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 1 DAY THEN id ELSE NULL END) AS active_1d,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 7 DAY THEN id ELSE NULL END) AS active_7d,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 14 DAY THEN id ELSE NULL END) AS active_14d,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 30 DAY THEN id ELSE NULL END) AS active_30d,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 60 DAY THEN id ELSE NULL END) AS active_60d,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 90 DAY THEN id ELSE NULL END) AS active_90d,
				COUNT(DISTINCT CASE WHEN last_active_date >= CURRENT_DATE() - INTERVAL 180 DAY THEN id ELSE NULL END) AS active_180d,
				COUNT(DISTINCT CASE WHEN last_active_date >= DATE_TRUNC('month', CURRENT_DATE()) THEN id ELSE NULL END) AS active_cur_month

FROM			klup_tmation.klupper
