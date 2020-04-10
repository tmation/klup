CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (

datestr VARCHAR(10),
activities_organized INTEGER,
activities_happened INTEGER,
organizer_count INTEGER,
active_organizer_count INTEGER,
attendees INTEGER,
active_attendees INTEGER,
friendships_created INTEGER,
downloads_google INTEGER,
downloads_apple INTEGER,
revenue_mollie INTEGER,
revenue_google INTEGER,
revenue_apple INTEGER,
users_paid INTEGER,
active_paying_users INTEGER,
trial_users INTEGER,
basic_users INTEGER,
--TODO Add earned users
referrals INTEGER,
daily_active_users INTEGER,
daily_signups INTEGER,
first_activity_users INTEGER,
dormant_users INTEGER,
active_1d INTEGER,
active_7d INTEGER,
active_14d INTEGER,
active_30d INTEGER,
active_60d INTEGER,
active_90d INTEGER,
active_180d INTEGER,
active_cur_month INTEGER,

_loaded_at DATETIME,

PRIMARY KEY(datestr)
)