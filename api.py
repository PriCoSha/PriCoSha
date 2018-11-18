from flask import request, Blueprint, session, jsonify, abort
from util import *

api = Blueprint('api', __name__)


@api.route('/loginAuth', methods=['POST'])
def login_auth():
    email = request.form['email']
    password = request.form['password']

    sql = '\
    SELECT fname, lname \
    FROM Person \
    WHERE email = %s AND password = %s;\
    '

    parameter = (email, password)
    data = query(sql, parameter)
    if data:
        # success
        session['email'] = email
        response = SuccessResponse(data[0])
    else:
        # error
        error = dict(code=1,
                     errormsg="Invalid login or email")
        response = ErrorResponse(error)
    return jsonify(response.__dict__)


@api.route('/logout', methods=['GET'])
def logout():
    if session.__len__() != 0:
        session.pop('email')
        response = SuccessResponse({"msg": "Log out successfully."})
    else:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/public_content', methods=['GET'])
def public_content():
    sql = '\
    SELECT item_name, item_id, email_post, post_time, file_path \
    FROM ContentItem \
    WHERE is_pub;\
    '  # TODO: ordered by descending time
    parameter = ()
    data = query(sql, parameter)
    response = SuccessResponse({"contentList": data})
    return jsonify(response.__dict__)


@api.route('/friendgroup', methods=['GET'])
def friendgroup():
    try:
        email = session['email']
        sql = '\
        SELECT owner_email, fg_name, description \
        FROM Belong NATURAL JOIN Friendgroup \
        WHERE email = %s;\
        '  # TODO: ordered by descending time
        parameter = (email)
        data = query(sql, parameter)
        response = SuccessResponse({"friendgroup": data})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/private_content', methods=['GET'])
def private_content():
    try:
        session['email']  # TODO: check if this person belongs to this friendgroup
        fg_name = request.args['fg_name']
        owner_email = request.args['owner_email']
        parameter = (fg_name, owner_email)
        sql = '\
        SELECT DISTINCT item_name, item_id, email_post, post_time, file_path \
        FROM ContentItem JOIN belong \
        WHERE (ContentItem.email_post = belong.owner_email) AND fg_name = %s AND belong.owner_email = %s;\
        '  # TODO: ordered by descending time, wrong sql!
        data = query(sql, parameter)
        response = SuccessResponse({"contentList": data})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 2, "errormsg": "invalid request"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/tag_count', methods=['GET'])
def tag_count():
    try:
        email = session['email']  # authenticate login
        sql = '\
        SELECT COUNT(*) AS tag_number \
        FROM Tag \
        WHERE email_tagged = %s AND status IS NULL;\
        '
        parameter = (email)
        data = query(sql, parameter)
        response = SuccessResponse(data[0])
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/tag', methods=['GET'])
def tag():
    try:
        email = session['email']  # authenticate login
        sql = '\
        SELECT email_tagger, item_name, file_path, tagtime \
        FROM Tag NATURAL JOIN ContentItem \
        WHERE email_tagged = %s AND status IS NULL;\
        '
        parameter = (email)
        data = query(sql, parameter)
        response = SuccessResponse({"tagList": data})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)



