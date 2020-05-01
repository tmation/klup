QUERY = """

SELECT DISTINCT
				datestr,
				activities_organized,
				activities_happened,
				organizer_count,
				active_organizer_count,
				attendees,
				active_attendees,
				friendships_created,
				downloads_google,
				downloads_apple,
				revenue_mollie,
				revenue_google,
				revenue_apple,
				users_paid,
				active_paying_users,
				trial_users,
				basic_users,
				referrals,
				daily_active_users,
				daily_signups,
				first_activity_users,
				dormant_users,
				active_1d,
				active_7d,
				active_14d,
				active_30d,
				active_60d,
				active_90d,
				active_180d,
				active_cur_month,
				
				friendships_active,
				friendships_created,
				friendships_created_7d,
				friendships_created_cur_month,
				earned_users,
					
				_loaded_at
				
FROM            {table_name}

WHERE           DATE(datestr) >= '{start_date}'

ORDER BY        1

"""