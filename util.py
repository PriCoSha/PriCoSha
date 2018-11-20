import pymysql.cursors
from time import time
from config import DB


class SuccessResponse(object):
    def __init__(self, data):
        self.state = True
        self.data = data
        self.timestamp = int(time())

    def __str__(self):
        return str(self.__dict__)


class ErrorResponse(object):
    def __init__(self, error):
        self.state = False
        self.error = error
        self.timestamp = int(time())

    def __str__(self):
        return str(self.__dict__)


def query(sql, parameter):
    connection = pymysql.connect(**DB)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, parameter)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result


def is_visible(item_id, email):
    parameter = (item_id, email)
    sql = '\
    SELECT item_id \
    FROM Belong NATURAL JOIN Share NATURAL JOIN ContentItem \
    WHERE item_id = %s AND (email = %s OR is_pub);\
    '
    data = query(sql, parameter)
    if data:
        return True
    return False


