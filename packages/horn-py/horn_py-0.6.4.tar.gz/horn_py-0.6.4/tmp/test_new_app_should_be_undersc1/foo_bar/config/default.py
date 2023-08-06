import os


PROJ_ROOT = os.path.split(os.path.abspath(__name__))[0]
LOG_CONF_PATH = os.path.join(PROJ_ROOT, 'logging.ini')
LOG_PATH = os.path.join(PROJ_ROOT, 'log')

SECRET_KEY = 'Ub3XfP_DWQWwGESi'
BCRYPT_LOG_ROUNDS = 13

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/foo_bar'
SQLALCHEMY_TRACK_MODIFICATIONS = False
