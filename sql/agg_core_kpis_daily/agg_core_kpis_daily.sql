-- SET SESSION MAX_JOIN_SIZE=20;
-- SET SESSION SQL_BIG_SELECTS=1;

SET STATEMENT SQL_BIG_SELECTS=1 FOR

WITH

dates AS (
	SELECT DISTINCT
	                dd.datestr,
	                dd.date

	FROM            klup_tmation.dim_date dd

	WHERE           1=1
	AND             dd.date BETWEEN '{START_DATE}' AND '{END_DATE}'
)

, activities AS (
	SELECT
	                klup_tmation.DATE_TRUNC('day', a.datetime_start) AS day,
	                COUNT(DISTINCT a.id) AS activities_organized,
	                COUNT(DISTINCT
	                    CASE
	                        WHEN a.is_cancelled = 0 THEN a.id
	                        ELSE NULL
                        END
                    ) AS activities_happened,
                    COUNT(DISTINCT a.klupper_id) AS organizer_count,
                    COUNT(DISTINCT
                        CASE
                            WHEN a.is_cancelled = 0 THEN a.klupper_id
                            ELSE NULL
                        END
                    ) AS active_organizer_count,
                    COUNT(DISTINCT ap.klupper_id) AS attendees,
                    COUNT(DISTINCT
                        CASE
                            WHEN a.is_cancelled = 0 THEN ap.klupper_id
                            ELSE NULL
                        END
                    ) AS active_attendees

    FROM            klup_tmation.activity a

	LEFT JOIN 		klup_tmation.activity_participant ap
	ON              a.id = ap.activity_id

	WHERE           1=1
	AND             a.datetime_start BETWEEN '{START_DATE}' AND '{END_DATE}'

	GROUP BY 1
)

, friendships AS (
	SELECT
					klup_tmation.DATE_TRUNC('day', d.datestr) AS day,
                    COUNT(DISTINCT f.id) AS friendships_created

    FROM			dates d

    LEFT JOIN		klup_tmation.friendship f
    ON				DATE(f.create_date) = d.datestr

    GROUP BY		1
)

, app_downloads AS (
	SELECT DISTINCT
					day AS day,
                    SUM(CASE WHEN adad.store = 'google_play' THEN adad.downloads ELSE 0 END) AS downloads_google,
                    SUM(CASE WHEN adad.store = 'apple' THEN adad.downloads ELSE 0 END) AS downloads_apple,
                    SUM(CASE WHEN adad.store = 'google_play' THEN adad.revenue ELSE 0 END) AS revenue_google,
                    SUM(CASE WHEN adad.store = 'apple' THEN adad.revenue ELSE 0 END) AS revenue_apple

    FROM			klup_tmation.agg_daily_app_store_data adad

	WHERE			1=1
    AND				day BETWEEN '{START_DATE}' AND '{END_DATE}'

    GROUP BY 		1
)

, revenues AS (
	SELECT DISTINCT
					klup_tmation.DATE_TRUNC('day', o.create_date) AS day,
					COUNT(DISTINCT o.klupper_id) AS paying_users,
					SUM(s.amount) AS revenue
	FROM			klup_tmation.ORDER o
	LEFT JOIN		klup_tmation.subscription s
	ON				s.id = o.subscription_id

	WHERE 			1=1
	AND				o.status = 'paid'
	AND				o.create_date BETWEEN '{START_DATE}' AND '{END_DATE}'
	GROUP BY 		1
)

, paying_users AS (
	SELECT
					d.date,
                    COUNT(DISTINCT m.klupper_id) AS paying_users
	FROM 			dates d
    LEFT JOIN 		membership m
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

	FROM			klup_tmation.klupper k

	LEFT JOIN 		klup_tmation.membership m
	ON				m.klupper_id = k.id

    LEFT JOIN 		analytics_active_klupper_details aakd
    ON				aakd.id = k.id

	WHERE			1=1

	GROUP BY 		1,2,3,4
)

, basic_trial_users AS (
	SELECT DISTINCT
					d.datestr AS day,
					COUNT(DISTINCT kf_trial.klupper_id) AS trial_users,
					COUNT(DISTINCT kf_basic.klupper_id) AS basic_users

	FROM			dates d

	LEFT JOIN 		klupper_frame kf_trial
	ON				kf_trial.had_paid_membership = 0
	AND				DATE(kf_trial.registration_date) <= DATE(d.datestr)
	AND				DATE(kf_trial.first_event_date) > DATE(d.datestr)
    AND				DATE(kf_trial.third_friend_request_date) > DATE(d.datestr)

	LEFT JOIN 		klupper_frame kf_basic
	ON				(
					kf_basic.had_paid_membership = 0
					AND	DATE(kf_basic.registration_date) >= DATE(d.datestr)
					AND	DATE(kf_basic.first_event_date) >= DATE(d.datestr)
                    AND DATE(kf_basic.third_friend_request_date) >= DATE(d.datestr)
					)
	OR 				(
					kf_basic.last_membership_end_date < d.datestr
					AND	DATE(kf_basic.registration_date) >= DATE(d.datestr)
					AND	DATE(kf_basic.first_event_date) >= DATE(d.datestr)
                    AND DATE(kf_basic.third_friend_request_date) >= DATE(d.datestr)
					)

	GROUP BY		1
)

, klupper_first_activity AS (
    SELECT DISTINCT
                    DATE(aakd.first_activity_date) AS datestr,
                    COUNT(DISTINCT aakd.id) AS first_activity_users

    FROM            analytics_active_klupper_details aakd

    WHERE           aakd.first_activity_date BETWEEN '{START_DATE}' AND '{END_DATE}'
)

SELECT
				d.datestr,

                -- Activities
                a.activities_organized AS activities_organized,
                a.activities_happened AS activities_happened,
                a.organizer_count AS organizer_count,
                a.active_organizer_count AS active_organizer_count,
                a.attendees AS attendees,
                a.active_attendees AS active_attendees,

                -- Friendships
                f.friendships_created AS friendships_created,

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
                btu.trial_users AS trial_users,
                btu.basic_users AS basic_users,
                0 AS referrals,
                0 AS daily_active_users,
                0 AS daily_signups,

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
                aubd.active_cur_month

FROM			dates d

LEFT JOIN 		activities a
ON 				DATE(a.day) = DATE(d.datestr)

LEFT JOIN		friendships f
ON				DATE(f.day) = DATE(d.datestr)

LEFT JOIN 		app_downloads ad
ON				DATE(ad.day) = DATE(d.datestr)

LEFT JOIN 		revenues r
ON				DATE(r.day) = DATE(d.datestr)

LEFT JOIN 		paying_users pu
ON				DATE(pu.date) = DATE(d.datestr)

LEFT JOIN		basic_trial_users btu
ON				DATE(btu.day) = DATE(d.datestr)

LEFT JOIN 		analytics_user_base_daily aubd
ON				DATE(aubd.datestr) = DATE(d.datestr)

LEFT JOIN 		klupper_first_activity kfa
ON 			 	DATE(kfa.datestr) = DATE(d.datestr)

GROUP BY 		1
;
