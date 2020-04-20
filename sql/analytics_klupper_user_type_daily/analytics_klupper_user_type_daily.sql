REPLACE INTO `{db_name}`.`{table_name}`

WITH

dates AS (
	SELECT DISTINCT
	                dd.datestr,
	                dd.date

	FROM            klup_tmation.dim_date dd

	WHERE           1=1
	AND             dd.date = '{DATE}'
)

, klupper_frame AS (
	SELECT 
					d.datestr,
					k.id,
					k.registration_date,
					m.begin_date AS membership_begin,
					m.end_date AS membership_end,
					aakd.third_friend_request_date,
                    k.last_active_date,
					CASE 
						WHEN aakd.is_invited = 1 THEN aakd.second_activity_date
						ELSE aakd.first_activity_date
					END AS first_event_date,
                    
                    CASE 
						WHEN 
							m.type = 'PAID' AND
							m.begin_date <= d.datestr AND
							m.end_date >= d.datestr 
							THEN TRUE
						ELSE FALSE
					END AS is_paid_member,

					CASE
						WHEN
							m.type = 'ADMIN' AND
							m.begin_date <= d.datestr AND
							m.end_date >= d.datestr
							THEN TRUE
						ELSE FALSE
					END AS is_admin_member,

					CASE
						WHEN
							m.type = 'SHARE' AND
							m.begin_date <= d.datestr AND
							m.end_date >= d.datestr
							THEN TRUE
						ELSE FALSE
					END AS is_share_member,

					CASE
						WHEN
							m.type = 'ORGANIZER' AND
							m.begin_date <= d.datestr AND
							m.end_date >= d.datestr
							THEN TRUE
						ELSE FALSE
					END AS is_organizer_member,
                    
                    CASE
						WHEN DATE(d.datestr) - INTERVAL '180' DAY >= k.last_active_date THEN TRUE
                        ELSE FALSE
					END AS is_dormant_member

	FROM 			dates d

	LEFT JOIN 		klupper k 
	ON 				1=1

	LEFT JOIN		membership m 
	ON				m.klupper_id = k.id

	LEFT JOIN		analytics_active_klupper_details aakd
	ON				aakd.id = k.id
)

, final AS (
	SELECT
					kf.datestr,
					kf.id,
					kf.is_dormant_member,
					kf.is_paid_member,
					kf.is_admin_member,
					kf.is_share_member,
					kf.is_organizer_member,

					CASE
						WHEN
							1=1
							AND kf.is_paid_member = FALSE
							AND kf.is_dormant_member = FALSE
							AND kf.is_admin_member = FALSE
							AND kf.is_share_member = FALSE
							AND kf.is_organizer_member = FALSE

							AND DATE(kf.registration_date) <= DATE(kf.datestr)
							AND (
								(DATE(kf.first_event_date) >= DATE(kf.datestr) OR kf.first_event_date IS NULL)
								OR (DATE(kf.third_friend_request_date) >= DATE(kf.datestr) OR kf.third_friend_request_date IS NULL)
								)
						THEN TRUE
						ELSE FALSE
					END AS is_trial_member,

					CASE
						WHEN
							1=1
							AND kf.is_paid_member = FALSE
							AND kf.is_dormant_member = FALSE
							AND kf.is_paid_member = FALSE
							AND kf.is_dormant_member = FALSE
							AND kf.is_admin_member = FALSE
							AND kf.is_share_member = FALSE
							AND kf.is_organizer_member = FALSE

							AND DATE(kf.registration_date) <= DATE(kf.datestr)
							AND DATE(kf.first_event_date) < DATE(kf.datestr)
							AND DATE(kf.third_friend_request_date) < DATE(kf.datestr)
						THEN TRUE
						ELSE FALSE
					END AS is_basic_member,
					CURRENT_TIMESTAMP AS _loaded_at

	--				,

	--                kf.registration_date,
	--                kf.first_event_date,
	--                kf.third_friend_request_date,
	--                kf.last_active_date,
	--                kf.membership_begin,
	--                kf.membership_end

	FROM			klupper_frame kf

	WHERE			DATE(kf.registration_date) <= DATE(kf.datestr)
)

SELECT
				f.datestr,
				f.id,
				f.is_dormant_member,
				f.is_paid_member,
				f.is_admin_member,
				f.is_share_member,
				f.is_organizer_member,

--				This section puts trial members as basic members before the release date of the new app
				CASE
					WHEN DATE(f.datestr) < '2020-04-17' THEN FALSE
					ELSE f.is_trial_member
				END AS is_trial_member,
				CASE
					WHEN DATE(f.datestr) < '2020-04-17' AND f.is_trial_member IS TRUE THEN TRUE
					ELSE f.is_basic_member
				END AS is_basic_member,
				f._loaded_at

FROM 			final f
