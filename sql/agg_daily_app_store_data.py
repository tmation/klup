ddl = """
CREATE TABLE IF NOT EXISTS klup_tmation.agg_daily_app_store_data (
	day varchar(10),
	store varchar(12),
	storefront varchar(12),
    downloads integer,
    re_downloads integer,
    edu_downloads integer,
	net_downloads integer,
    uninstalls integer,
    updates integer,
    gross_revenue float,
	gross_edu_revenue float,
	revenue float,
	gift_redemptions float,
	promos float,
	gifts float,
	returns float,
	edu_revenue float,
	returns_amount float,
	gross_returns_amount float,
	_loaded_at datetime,
    
    PRIMARY KEY (day, store)
)
"""

replace = """
REPLACE INTO `klup_tmation`.`agg_daily_app_store_data` VALUES (
    %(day)s,
    %(store)s,
    %(storefront)s,
    %(downloads)s,
    %(re_downloads)s,
    %(edu_downloads)s,
	%(net_downloads)s,
    %(uninstalls)s,
    %(updates)s,
    %(gross_revenue)s,
	%(gross_edu_revenue)s,
	%(revenue)s,
	%(gift_redemptions)s,
	%(promos)s,
	%(gifts)s,
	%(returns)s,
	%(edu_revenue)s,
	%(returns_amount)s,
	%(gross_returns_amount)s,
	%(_loaded_at)s
);
"""