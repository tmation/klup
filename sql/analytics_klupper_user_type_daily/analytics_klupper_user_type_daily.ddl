CREATE TABLE IF NOT EXISTS `klup_tmation`.`{table_name}` (
	datestr VARCHAR(10),
	id INTEGER,
  is_dormant_member BOOLEAN,
	is_paid_member BOOLEAN,
	is_trial_member BOOLEAN,
	is_basic_member BOOLEAN,

	_loaded_at DATETIME,

PRIMARY KEY(datestr, id)
)

