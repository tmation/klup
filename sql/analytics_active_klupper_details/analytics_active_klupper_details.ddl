CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (
	id INTEGER,
	is_invited BOOLEAN,
	third_friend_request_date DATETIME,
	first_activity_date DATETIME,
	second_activity_date DATETIME,
	activity_visited INTEGER,
	friendship_count INTEGER,
	_loaded_at DATETIME,

PRIMARY KEY(id)
)
