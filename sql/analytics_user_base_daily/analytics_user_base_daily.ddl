CREATE TABLE IF NOT EXISTS klup_tmation.analytics_user_base_daily (
	datestr varchar(10),
	dormant_users integer,
	active_1d integer,
	active_7d integer,
    active_14d integer,
    active_30d integer,
    active_60d integer,
	active_90d integer,
    active_180d integer,
    active_cur_month integer,

    PRIMARY KEY (datestr)
)