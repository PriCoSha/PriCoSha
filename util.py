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
    FROM Belong NATURAL RIGHT JOIN Share NATURAL RIGHT JOIN ContentItem \
    WHERE item_id = %s AND (email = %s OR is_pub);\
    '
    data = query(sql, parameter)
    if data:
        return True
    return False


def check_belong(email, fg_name, owner_email):
    parameter = (email, fg_name, owner_email)
    sql = '\
    SELECT owner_email, fg_name \
    FROM Belong \
    WHERE email = %s AND fg_name = %s AND owner_email = %s;\
    '
    data = query(sql, parameter)
    if data:
        return True
    return False


def is_group_visible(owner_email, fg_name, item_id):
    parameter = (owner_email, fg_name, item_id)
    sql = '\
    SELECT * \
    FROM Share \
    WHERE owner_email = %s AND fg_name = %s AND item_id = %s;\
    '
    data = query(sql, parameter)
    if data:
        return True
    return False


def is_request_exist(email_tagged, email_tagger, owner_email, fg_name, item_id):
    parameter = (email_tagged, email_tagger, owner_email, fg_name, item_id)
    sql = '\
    SELECT * FROM GroupTagPending \
    WHERE email_tagged = %s AND email_tagger = %s AND owner_email = %s AND fg_name = %s AND item_id = %s;\
    '
    data = query(sql, parameter)
    if data:
        return True
    return False