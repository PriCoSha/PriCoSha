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
    WHERE is_pub AND NOW()-post_time < 12960000 \
    ORDER BY post_time DESC;\
    '
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
        '
        parameter = (email)
        data = query(sql, parameter)
        response = SuccessResponse({"friendgroup": data})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/private_content', methods=['GET'])
def private_content():
    fg_name = request.args['fg_name']
    owner_email = request.args['owner_email']
    try:
        email = session['email']
        parameter = (email, fg_name, owner_email)
        sql = '\
        SELECT owner_email, fg_name \
        FROM Belong \
        WHERE email = %s AND fg_name = %s AND owner_email = %s;\
        '
        data = query(sql, parameter)
        if data:
            pass
        else:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
        return jsonify(response.__dict__)

    try:
        parameter = (fg_name, owner_email)
        sql = '\
        SELECT item_name, item_id, email_post, post_time, file_path \
        FROM ContentItem NATURAL JOIN share \
        WHERE fg_name = %s AND owner_email = %s \
        ORDER BY post_time DESC;\
        '
        data = query(sql, parameter)
        response = SuccessResponse({"contentList": data})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 2, "errormsg": "invalid request"})
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


@api.route('/pending_tag', methods=['GET'])
def pending_tag():
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


@api.route('/tag', methods=['PATCH'])
def tag_patch():
    try:
        email = session['email']
        status = request.form['status']
        email_tagged = request.form['email_tagged']
        email_tagger = request.form['email_tagger']
        item_id = request.form['item_id']
        if email != email_tagged:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        parameter = (status, email_tagged, email_tagger, item_id)
        sql = '\
        UPDATE Tag \
        SET status = %s \
        WHERE email_tagged = %s AND email_tagger = %s AND item_id = %s;\
        '
        data = query(sql, parameter)  # TODO: potential risk, non-existent tag
        response = SuccessResponse({"msg": "Successfully updated"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 5, "errormsg": "invalid parameter, please check"})
    return jsonify(response.__dict__)


@api.route('/rate', methods=['GET'])
def get_rate():
    item_id = request.args['item_id']
    try:
        email = session['email']
    except KeyError:
        email = 'guest'
    if is_visible(item_id, email):
        sql = '\
        SELECT email, emoji, rate_time \
        FROM Rate \
        WHERE item_id = %s \
        ORDER BY rate_time DESC;\
        '
        parameter = (item_id)
        data = query(sql, parameter)
        response = SuccessResponse({"rateList": data})
    else:
        response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
    return jsonify(response.__dict__)


@api.route('/rate', methods=['GET'])
def get_tag():
    item_id = request.args['item_id']
    try:
        email = session['email']
    except KeyError:
        email = 'guest'
    if is_visible(item_id, email):
        sql = '\
        SELECT email_tagger, email_tagged, tagtime \
        FROM Tag \
        WHERE item_id = %s AND status = 1 \
        ORDER BY tagtime DESC;\
        '
        parameter = (item_id)
        data = query(sql, parameter)
        response = SuccessResponse({"tagList": data})
    else:
        response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
    return jsonify(response.__dict__)


# TODO: /tag POST


# TODO: /item POST


# TODO: /friendgroup PATCH (add a member to a friendgroup)
@api.route('/friendgroup', methods=['PATCH'])
def add_friend():
    fg_name = request.form['fg_name']
    owner_email = request.form['owner_email']

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')

    try:
        session_email = session['email']
        if session_email != owner_email:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        if email:  # insert using email
            parameter = (email, owner_email, fg_name)
            sql = '\
            INSERT INTO Belong(email, owner_email, fg_name) \
            VALUES (%s, %s, %s);\
            '
            query(sql, parameter)
            response = SuccessResponse({"msg": "New member successfully added."})
        elif fname and lname: # insert using fname and lname
            # find this person's email first:
            sql = '\
            SELECT email \
            FROM Person \
            WHERE fname = %s AND lname = %s;\
            '
            parameter = (fname, lname)
            data = query(sql, parameter)
            if len(data) == 0:
                response = ErrorResponse({"code": 7, "errormsg": "Person not found"})
            elif len(data) == 1:
                parameter = (data[0]['email'], owner_email, fg_name)
                sql = '\
                INSERT INTO Belong(email, owner_email, fg_name) \
                VALUES (%s, %s, %s);\
                '
                query(sql, parameter)
                response = SuccessResponse({"msg": "New member successfully added."})
            else:
                response = ErrorResponse({"code": 8, "errormsg": "Multiple persons found, use email instead."})
        else:
            abort(400)
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 6, "errormsg": "This person is already in the group"})
    return jsonify(response.__dict__)
