import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://username:password@localhost/shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
