
# Flask core settings
DEBUG = True
TESTING = False
#SECRET_KEY = ''
PERMANENT_SESSION_LIFETIME = 60*60*24*30 # One month

# flask wtf settings
#WTF_CSRF_ENABLED = True

# flask mail settings
MAIL_DEFAULT_SENDER = 'noreply@yourmail.com'

# project settings
#PROJECT_PASSWORD_HASH_METHOD = ''
#PROJECT_SITE_NAME = u'GURGIWS1'
#PROJECT_SITE_URL = u'http://127.0.0.1:5000'
#PROJECT_SIGNUP_TOKEN_MAX_AGE = 60 * 60 * 25 * 7 # in s
#PROJECT_RECOVER_PASSWORD_TOKEN_MAX_AGE = 60*60*24*7

# db settings
MONGODB_DB = "gurgi_db"

API_URL = ""
#CPP_SERVER_URL = "http:/127.0.0.1:80"
#API_HEADERS = {}
#OPERATION_CODES = {'MAX_HUMID':1,
# }