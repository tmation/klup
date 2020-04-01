REPLACE INTO `{db_name}`.`{table_name}`

WITH

klupper_first_event_prep AS (
	SELECT DISTINCT
					k.id AS klupper_id,
					CASE
						WHEN k.invited_by IS NOT NULL THEN TRUE
						ELSE FALSE
					END AS is_invited,
					ap.activity_id,
					COALESCE(a.datetime_end, a.datetime_start) AS event_date,
					ROW_NUMBER() OVER (PARTITION BY k.id ORDER BY COALESCE(a.datetime_end, a.datetime_start) ASC) AS activity_rank


	FROM			klupper k

	LEFT JOIN		activity_participant ap
	ON				k.id = ap.klupper_id

	LEFT JOIN		activity a
	ON 				ap.activity_id = a.id

	WHERE			1=1
)

, klupper_friend_requests_prep AS (
	SELECT DISTINCT
					f.sender_id AS klupper_id,
                    f.id AS friendship_id,
                    create_date AS friend_request_create_date,
					ROW_NUMBER() OVER (PARTITION BY sender_id ORDER BY create_date ASC) AS friend_request_rank

	FROM			friendship f
)

SELECT DISTINCT
				k.id,
                kfep1.is_invited,
                kfrp1.friend_request_create_date AS third_friend_request_date,
                MAX(CASE WHEN kfep1.activity_rank = 1 THEN kfep1.event_date END) AS first_activity_date,
                MAX(CASE WHEN kfep1.activity_rank = 2 THEN kfep1.event_date END) AS second_activity_date,
                COUNT(DISTINCT kfep1.activity_id) AS activity_visited,
                COUNT(DISTINCT kfrp2.friendship_id) AS friendship_count


FROM			klupper k

LEFT JOIN 		klupper_first_event_prep kfep1
ON				kfep1.klupper_id = k.id
AND				kfep1.activity_rank <= 2

LEFT JOIN 		klupper_first_event_prep kfep2
ON				kfep2.klupper_id = k.id

LEFT JOIN		klupper_friend_requests_prep kfrp1
ON				kfrp1.klupper_id = k.id
AND				kfrp1.friend_request_rank = 3

LEFT JOIN		klupper_friend_requests_prep kfrp2
ON				kfrp2.klupper_id = k.id

WHERE			1=1
AND				k.status = 'NORMAL'

GROUP BY 		1,2,3

