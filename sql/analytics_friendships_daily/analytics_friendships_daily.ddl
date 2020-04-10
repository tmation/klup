CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (

	datestr varchar(10),
	friendships_active integer,
	friendships_created integer,
	friendships_created_1d integer,
	friendships_created_7d integer,
	friendships_created_14d integer,
	friendships_created_30d integer,
	friendships_created_60d integer,
	friendships_created_90d integer,
	friendships_created_180d integer,
	friendships_created_cur_month integer,

	_loaded_at DATETIME,

PRIMARY KEY(datestr)
)