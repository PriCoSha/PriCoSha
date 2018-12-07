import pymysql


class Config:
    SECRET_KEY = 'FrankGPA4'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    threaded = True
    host = 'localhost'
    port = 5000


DB = {'host': 'localhost',
      'port': 8889,
      'user': 'root',
      'password': 'root',
      'db': 'pricosha',
      'charset': 'utf8mb4',
      'cursorclass': pymysql.cursors.DictCursor
      }  # local MAMP DB

config = dict(development=DevelopmentConfig)
