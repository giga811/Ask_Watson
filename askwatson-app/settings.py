"""Config"""

# APP Folder
PATH = '/tmp/askwatson/'

### Variables
DATABASE = PATH + 'askwatson.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'askwatson' # secret key for app

# mysql settings
MYSQL_DATABASE_HOST = 'localhost'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_USER = 'watson'
MYSQL_DATABASE_PASSWORD = 'askwatson'
MYSQL_DATABASE_DB = 'askwatson'
MYSQL_DATABASE_CHARSET = 'utf8'
# format is dialect+driver://username:password@host:port/database
# SQLALCHEMY_DATABASE_URI = 'mysql://goomaral:bluespot@localhost/bluespot'
SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///' + DATABASE

# file upload config
UPLOAD_FOLDER = PATH + 'upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024