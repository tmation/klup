insert_table = """
REPLACE INTO klup_tmation.agg_daily_app_data
    VALUES (
        %(day)s,
        %(store)s,
        %(user_installs)s,
        %(user_uninstalls)s,
        %(total_user_installs)s,
        %(device_installs)s,
        %(device_uninstalls)s,
        %(active_device_installs)s,
        %(install_events)s,
        %(update_events)s,
        %(uninstall_events)s
    )
"""