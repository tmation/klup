ddl_table = """
CREATE TABLE IF NOT EXISTS `klup_tmation`.`agg_daily_app_data` (
    `day` varchar(10),
    `store` varchar(10),
    `user_installs` int,
    `user_uninstalls` int,
    `total_user_installs` int,
    `device_installs` int,
    `device_uninstalls` int,
    `active_device_installs` int,
    `install_events` int,
    `update_events` int,
    `uninstall_events` int,
    
    PRIMARY KEY (`day`, `store`)
);
"""