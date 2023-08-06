from datetime import timedelta

from .default import *          # NOQA F401


ENV = 'development'
DEBUG = True
JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/ohmygod_dev'
