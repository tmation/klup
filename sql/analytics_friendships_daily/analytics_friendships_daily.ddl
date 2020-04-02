CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (

	datestr varchar(10),
	friendships_active integer,
	friendships_created integer,

	_loaded_at DATETIME,

PRIMARY KEY(datestr)
)