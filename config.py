from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

print(basedir)
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')
    API_AUDIENCE = environ.get('API_AUDIENCE')
    ALGORITHMS = environ.get('ALGORITHMS')
    ALGORITHMS = ALGORITHMS.split(';')[:-1]
    MAILBOX_PATH = environ.get('MAILBOX_PATH')
    MAIL_USER = environ.get('MAIL_USER')
    PAYLOAD = environ.get('PAYLOAD')

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')