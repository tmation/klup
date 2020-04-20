import os

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
	AF_ACCESS_TOKEN = os.environ.get('AF_ACCESS_TOKEN', None)
	AF_ACCESS_TOKEN_SECRET = os.environ.get('AF_ACCESS_TOKEN_SECRET', None)
	AF_CLIENT_ID = os.environ.get('AF_CLIENT_ID', None)
	AF_CLIENT_SECRET = os.environ.get('AF_CLIENT_SECRET', None)

	DB_KLUP_HOST = os.environ.get('DB_KLUP_HOST', None)
	DB_KLUP_NAME = os.environ.get('DB_KLUP_NAME', None)
	DB_KLUP_PASSWORD = os.environ.get('DB_KLUP_PASSWORD', None)
	DB_KLUP_USER = os.environ.get('DB_KLUP_USER', None)

	# GOOGLE_SVC_TMATION = os.environ.get('GOOGLE_SVC_TMATION', None)

else:
	import creds
	AF_ACCESS_TOKEN = creds.AF_ACCESS_TOKEN
	AF_ACCESS_TOKEN_SECRET = creds.AF_ACCESS_TOKEN_SECRET
	AF_CLIENT_ID = creds.AF_CLIENT_ID
	AF_CLIENT_SECRET = creds.AF_CLIENT_SECRET

	DB_KLUP_HOST = creds.DB_KLUP_HOST
	DB_KLUP_NAME = creds.DB_KLUP_NAME
	DB_KLUP_PASSWORD = creds.DB_KLUP_PASSWORD
	DB_KLUP_USER = creds.DB_KLUP_USER

	# DB_KLUP_HOST = creds.DB_KLUP_HOST
	# DB_KLUP_NAME = creds.DB_KLUP_STAG_NAME
	# DB_KLUP_PASSWORD = creds.DB_KLUP_STAG_PASSWORD
	# DB_KLUP_USER = creds.DB_KLUP_STAG_USER

	# GOOGLE_SVC_TMATION = creds.GOOGLE_SVC_TMATION
	os.environ['GOOGLE_SVC_TMATION'] = creds.GOOGLE_SVC_TMATION
