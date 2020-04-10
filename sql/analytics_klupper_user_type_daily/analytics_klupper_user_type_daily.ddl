CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (
	datestr VARCHAR(10),
	id INTEGER,
  is_dormant_member BOOLEAN,
	is_paid_member BOOLEAN,
	is_admin_member BOOLEAN,
	is_share_member BOOLEAN,
	is_organizer_member BOOLEAN,
	is_trial_member BOOLEAN,
	is_basic_member BOOLEAN,

	_loaded_at DATETIME,

PRIMARY KEY(datestr, id)
)

