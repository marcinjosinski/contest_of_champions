import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'grandmaster-likes-to-dance'
    DATABASE = 'area'
    DB_PASSWORD = 'coc-pass'
    DB_USERNAME = 'coc-user'
    DB_HOSTNAME = 'mysql'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:3306/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
