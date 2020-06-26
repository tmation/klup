-- SET SESSION MAX_JOIN_SIZE=20;
-- SET SESSION SQL_BIG_SELECTS=1;

SET STATEMENT SQL_BIG_SELECTS=1 FOR

REPLACE INTO `{db_name}`.`{table_name}`

WITH

dates AS (
	SELECT DISTINCT
	                dd.datestr,
	                dd.date

	FROM            {db_name}.dim_date dd

	WHERE           1=1
	AND             dd.date BETWEEN '{START_DATE}' AND '{END_DATE}'
)

, activities AS (
	SELECT
	                {db_name}.DATE_TRUNC('{TIME_INTERVAL}', a.datetime_start) AS day,
	                COUNT(DISTINCT a.id) AS activities_organized,
	                COUNT(DISTINCT
	                    CASE
	                        WHEN a.is_cancelled = 0 AND a.status != 'DELETED' THEN a.id
	                        ELSE NULL
                        END
                    ) AS activities_happened,
                    COUNT(DISTINCT a.klupper_id) AS organizer_count,
                    COUNT(DISTINCT
                        CASE
                            WHEN a.is_cancelled = 0 AND a.status != 'DELETED' THEN a.klupper_id
                            ELSE NULL
                        END
                    ) AS active_organizer_count,
                    COUNT(DISTINCT ap.klupper_id) AS attendees,
                    COUNT(DISTINCT
                        CASE
                            WHEN a.is_cancelled = 0 AND a.status != 'DELETED' THEN ap.klupper_id
                            ELSE NULL
                        END
                    ) AS active_attendees

    FROM            {db_name}.activity a
    LEFT JOIN 		{db_name}.activity_participant ap
	ON              a.id = ap.activity_id

	WHERE           1=1
	AND             a.datetime_start BETWEEN '{START_DATE}' AND '{END_DATE}'

	GROUP BY 		1
)

, app_downloads AS (
	SELECT DISTINCT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', adad.day) AS day,
                    SUM(CASE WHEN adad.store = 'google_play' THEN adad.downloads ELSE 0 END) AS downloads_google,
                    SUM(CASE WHEN adad.store = 'apple' THEN adad.downloads ELSE 0 END) AS downloads_apple,
                    SUM(CASE WHEN adad.store = 'google_play' THEN adad.revenue ELSE 0 END) AS revenue_google,
                    SUM(CASE WHEN adad.store = 'apple' THEN adad.revenue ELSE 0 END) AS revenue_apple

    FROM			{db_name}.agg_daily_app_store_data adad

	WHERE			1=1
    AND				day BETWEEN '{START_DATE}' AND '{END_DATE}'

    GROUP BY 		1
)

, revenues AS (
	SELECT DISTINCT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', o.create_date) AS day,
					COUNT(DISTINCT o.klupper_id) AS paying_users,
					SUM(s.amount) AS revenue

	FROM			{db_name}.ORDER o
	LEFT JOIN		{db_name}.subscription s
	ON				s.id = o.subscription_id

	WHERE 			1=1
	AND				o.status = 'paid'
	AND				o.create_date BETWEEN '{START_DATE}' AND '{END_DATE}'
	GROUP BY 		1
)

, paying_users AS (
	SELECT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', d.date) AS date,
                    COUNT(DISTINCT m.klupper_id) AS paying_users

	FROM 			dates d

    LEFT JOIN 		{db_name}.membership m
    ON				DATE(d.datestr) >= DATE(m.begin_date)
    AND				DATE(d.datestr) < DATE(m.end_date)
    AND 			m.type = 'PAID'

    GROUP BY 		1
)

, klupper_frame AS (
	SELECT DISTINCT
					k.id AS klupper_id,
					k.registration_date,
					CASE
						WHEN aakd.is_invited = TRUE THEN aakd.second_activity_date
                        WHEN aakd.is_invited = FALSE THEN aakd.first_activity_date
                        ELSE NULL
					END AS first_event_date,
                    aakd.third_friend_request_date,
					COUNT(DISTINCT
						CASE
							WHEN m.type = 'PAID' THEN k.id
                            ELSE NULL
					END) AS had_paid_membership,
                    MAX(m.end_date) AS last_membership_end_date

	FROM			{db_name}.klupper k

	LEFT JOIN 		{db_name}.membership m
	ON				m.klupper_id = k.id

    LEFT JOIN 		{db_name}.analytics_active_klupper_details aakd
    ON				aakd.id = k.id

	WHERE			1=1

	GROUP BY 		1,2,3,4
)

, user_type_counts AS (
	SELECT DISTINCT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', akutd.datestr) AS day,
					COUNT(DISTINCT CASE
						WHEN akutd.is_trial_member = TRUE THEN akutd.id
						ELSE NULL
					END) AS trial_users,

					COUNT(DISTINCT CASE
						WHEN akutd.is_basic_member = TRUE THEN akutd.id
						ELSE NULL
					END) AS basic_users,

					COUNT(DISTINCT CASE
						WHEN akutd.is_paid_member = TRUE THEN akutd.id
						ELSE NULL
					END) AS paid_users,

					COUNT(DISTINCT CASE
						WHEN akutd.is_admin_member = TRUE
							OR akutd.is_share_member = TRUE
							OR akutd.is_organizer_member = TRUE
							THEN akutd.id
						ELSE NULL
					END) AS earned_users

	FROM			analytics_klupper_user_type_daily akutd

	WHERE			1=1
	AND				DATE(akutd.datestr) BETWEEN '{START_DATE}' AND '{END_DATE}'

	GROUP BY		1
)

, klupper_first_activity AS (
    SELECT DISTINCT
                    {db_name}.DATE_TRUNC('{TIME_INTERVAL}', DATE(aakd.first_activity_date)) AS datestr,
                    COUNT(DISTINCT aakd.id) AS first_activity_users

    FROM            {db_name}.analytics_active_klupper_details aakd

    WHERE           aakd.first_activity_date BETWEEN '{START_DATE}' AND '{END_DATE}'

    GROUP BY 		1
)

, klupper_sign_ups AS (
	SELECT DISTINCT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', DATE(k.registration_date)) AS datestr,
					COUNT(DISTINCT k.id) AS daily_signups

	FROM			{db_name}.klupper k

	WHERE			k.registration_date BETWEEN '{START_DATE}' AND '{END_DATE}'

	GROUP BY 		1
)

, moments AS (
	SELECT DISTINCT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', DATE(m.create_date)) AS datestr,
					COUNT(DISTINCT m.id) AS moments_created

	FROM			{db_name}.moment m

	WHERE			m.create_date BETWEEN '{START_DATE}' AND '{END_DATE}'

	GROUP BY 		1
)

, first_membership_rank AS (
	SELECT
					*,
					ROW_NUMBER() OVER (PARTITION BY m.klupper_id ORDER BY m.begin_date ASC) AS rn

	FROM			{db_name}.membership m

	WHERE 			m.type IN ('ADMIN','PAID')
)

, first_memberships AS (
	SELECT
					{db_name}.DATE_TRUNC('{TIME_INTERVAL}', fm.begin_date) AS datestr,
					COUNT(DISTINCT fm.klupper_id) AS first_membership_count

	FROM 			first_membership_rank fm

	WHERE 			rn = 1
	AND				fm.begin_date BETWEEN '{START_DATE}' AND '{END_DATE}'

	GROUP BY 		1

)

SELECT
				DATE({db_name}.DATE_TRUNC('{TIME_INTERVAL}', d.datestr)),

                -- Activities
                a.activities_organized AS activities_organized,
                a.activities_happened AS activities_happened,
                a.organizer_count AS organizer_count,
                a.active_organizer_count AS active_organizer_count,
                a.attendees AS attendees,
                a.active_attendees AS active_attendees,

                -- Friendships
                afd.friendships_active AS friendships_active,
                afd.friendships_created AS friendships_created,
                afd.friendships_created_7d AS friendships_created_7d,
                afd.friendships_created_cur_month AS friendships_created_cur_month,

                -- App Downloads
                ad.downloads_google,
                ad.downloads_apple,

                -- Financials
                r.revenue AS revenue_mollie,
                ad.revenue_google AS revenue_google,
                ad.revenue_apple AS revenue_apple,

                -- Users
                r.paying_users AS users_paid,
                pu.paying_users AS active_paying_users,
                utc.trial_users AS trial_users,
                utc.basic_users AS basic_users,
                utc.earned_users AS earned_users,
                0 AS referrals,
                0 AS daily_active_users,
                ksu.daily_signups AS daily_signups,

                kfa.first_activity_users,

                -- User Base
				aubd.dormant_users,
                aubd.active_1d,
                aubd.active_7d,
                aubd.active_14d,
                aubd.active_30d,
                aubd.active_60d,
                aubd.active_90d,
                aubd.active_180d,
                aubd.active_cur_month,

                CURRENT_TIMESTAMP AS _loaded_at,

                m.moments_created AS moments_created,
                fm.first_membership_count AS first_membership_count

FROM			dates d

LEFT JOIN 		activities a
ON 				DATE(a.day) = DATE(d.datestr)

LEFT JOIN		analytics_friendships_daily afd
ON				DATE(afd.datestr) = DATE(d.datestr)

LEFT JOIN 		app_downloads ad
ON				DATE(ad.day) = DATE(d.datestr)

LEFT JOIN 		revenues r
ON				DATE(r.day) = DATE(d.datestr)

LEFT JOIN 		paying_users pu
ON				DATE(pu.date) = DATE(d.datestr)

LEFT JOIN 		user_type_counts utc
ON				DATE(utc.day) = DATE(d.datestr)

LEFT JOIN 		analytics_user_base_daily aubd
ON				DATE(aubd.datestr) = DATE(d.datestr)

LEFT JOIN 		klupper_first_activity kfa
ON 			 	DATE(kfa.datestr) = DATE(d.datestr)

LEFT JOIN		klupper_sign_ups ksu
ON				DATE(ksu.datestr) = DATE(d.datestr)

LEFT JOIN 		moments m
ON				DATE(m.datestr) = DATE(d.datestr)

LEFT JOIN		first_memberships fm
ON				DATE(fm.datestr) = DATE(d.datestr)

GROUP BY 		1
;
