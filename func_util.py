import sys
sys.path.append('..')
sys.path.append('/submodules')

import config
from appfigures_py import appfigures_py

af = appfigures_py.AppFigures(config.appfigures_secrets['client_id'], config.appfigures_secrets['client_secret'])
af.get_session(config.appfigures_secrets['access_token'], config.appfigures_secrets['access_token_secret'])

