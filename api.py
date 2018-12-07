from flask import request, Blueprint, session, jsonify, abort
from util import *

api = Blueprint('api', __name__)


@api.route('/member', methods=['GET'])
def get_member():
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
        SELECT * \
        FROM Belong \
        WHERE fg_name = %s AND owner_email = %s \
        '
        data = query(sql, parameter)
        response = SuccessResponse({"contentList": data})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 2, "errormsg": "invalid request"})
    return jsonify(response.__dict__)


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


@api.route('/name', methods=['GET'])
def get_name():
    try:
        email = session['email']
        sql = '\
        SELECT fname, lname \
        FROM Person \
        WHERE email = %s\
        '
        parameter = (email)
        data = query(sql, parameter)
        print(data)
        response = SuccessResponse(data[0])
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
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
    SELECT *\
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
        SELECT * \
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
        query(sql, parameter)  # TODO: potential risk, non-existent tag
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


@api.route('/tag', methods=['GET'])
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


@api.route('/tag', methods=['POST'])
def post_tag():
    email_tagged = request.form['email_tagged']
    email_tagger = request.form['email_tagger']
    item_id = request.form['item_id']

    try:
        session_email = session['email']
        # authenticate user's identity
        if session_email != email_tagger:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        # authenticate if tagged can see the content
        if is_visible(item_id, email_tagger) and is_visible(item_id, email_tagged):
            sql = '\
            INSERT INTO Tag(email_tagged, email_tagger, item_id, status) \
            VALUES(%s,%s,%s,%s);\
            '
            if email_tagger == email_tagged:
                status = '1'
                msg = "Self Tag Successfully Posted."
            else:
                status = None
                msg = "Tag Successfully Posted, waiting for taggee's approval."
            parameter = (email_tagged, email_tagger, item_id, status)
            query(sql, parameter)
            response = SuccessResponse({"msg": msg})
        else:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/content', methods=['POST'])
def post_content():
    owner_emails = request.form['owner_emails'].split(';')
    fg_names = request.form['fg_names'].split(';')
    if len(owner_emails) != len(fg_names):
        response = ErrorResponse({"code": 7, "errormsg": "fg_name and owner_email do not match."})
        return jsonify(response.__dict__)
    file_path = request.form['file_path']
    item_name = request.form['item_name']
    is_pub = int(request.form['is_pub'])
    if is_pub:
        is_pub = True
    else:
        is_pub = False
    email_post = request.form['email_post']

    try:
        session_email = session['email']
        # authenticate user's identity
        if session_email != email_post:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        sql = '\
        INSERT INTO ContentItem(email_post, file_path, item_name, is_pub) \
        VALUES(%s, %s, %s, %s); \
        '
        parameter = (email_post, file_path, item_name, is_pub)
        query(sql, parameter)
        sql = '\
        SELECT item_id \
        FROM ContentItem \
        WHERE email_post = %s AND file_path = %s AND item_name = %s AND is_pub = %s \
        ORDER BY post_time DESC;\
        '
        data = query(sql, parameter)
        item_id = data[0]["item_id"]

        fg_error = []
        for i in range(len(owner_emails)):
            if not check_belong(email_post, fg_names[i], owner_emails[i]):
                fg_error.append((owner_emails[i], fg_names[i]))
                continue
            try:
                parameter = (owner_emails[i], fg_names[i], item_id)
                sql = '\
                INSERT INTO Share(owner_email, fg_name, item_id) \
                VALUES (%s, %s, %s);\
                '
                query(sql, parameter)
            except pymysql.err.IntegrityError:
                fg_error.append((owner_emails[i], fg_names[i]))

        if fg_error:
            response = SuccessResponse({"msg": "Item successfully posted,"
                                               " but some it can't be shared to the following friendgroup",
                                        "item_id": item_id,
                                        "error_fg": fg_error})
        else:
            response = SuccessResponse({"msg": "Item successfully posted", "item_id": item_id})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/friendgroup', methods=['PATCH'])
def add_friend():
    fg_name = request.form['fg_name']
    owner_email = request.form['owner_email']

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')

    try:
        session_email = session['email']
        response = None
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


"""
EXTRA FEATURE BEGINS HERE
"""


@api.route('/rate', methods=['POST'])  # This route is for extra feature: Post comment
def post_rate():
    rater_email = request.form['rater_email']
    item_id = request.form['item_id']
    emoji = request.form['emoji']
    try:
        session_email = session['email']
        # authenticate user's identity
        if session_email != rater_email:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        # authenticate if tagged can see the content
        if is_visible(item_id, rater_email):
            sql = '\
            INSERT INTO Rate(email, item_id, emoji) \
            VALUES (%s, %s, %s);\
            '
            parameter = (rater_email, item_id, emoji)
            query(sql, parameter)
            response = SuccessResponse({"msg": "Comment successfully posted."})
        else:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/friendgroup', methods=['DELETE'])  # This route is for removing a member from a friend group
def defriend():
    fg_name = request.form['fg_name']
    owner_email = request.form['owner_email']
    email = request.form['email']  # email of the user that need to be removed
    try:
        session_email = session['email']
        if session_email != owner_email or not check_belong(email, fg_name, owner_email):
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)

        # first of all, find all the contentitem that is no more visible to this user
        sql = '\
        SELECT email_tagged, email_tagger, item_id \
        FROM Tag NATURAL JOIN Share \
        WHERE (email_tagged = %s OR email_tagger = %s) AND owner_email = %s AND fg_name = %s;\
        '
        parameter = (email, email, owner_email, fg_name)
        data = query(sql, parameter)  # items that the user can no longer see
        for item in data:  # remove the tags that he can no longer see.
            parameter = (item['email_tagged'], item['email_tagger'], item['item_id'])
            sql = '\
            DELETE FROM Tag \
            WHERE email_tagged = %s AND email_tagger = %s AND item_id = %s;\
            '
            query(sql, parameter)
        # delete this user from the user group
        parameter = (email, owner_email, fg_name)
        sql = '\
        DELETE FROM Belong \
        WHERE email = %s AND owner_email = %s AND fg_name = %s;\
        '
        query(sql, parameter)
        response = SuccessResponse({"msg": "This person has been successfully removed from the group"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


#############################
#        GROUP TAGS         #
#############################

@api.route('/grouptag', methods=['POST'])
def post_group_tag():
    email_tagger = request.form['email_tagger']
    fg_name = request.form['fg_name']
    owner_email = request.form['owner_email']
    item_id = request.form['item_id']
    try:
        session_email = session['email']
        # authenticate user's identity
        if session_email != email_tagger:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        if is_visible(item_id, email_tagger) and is_group_visible(owner_email, fg_name, item_id):
            # insert a new pending group tag
            sql = '\
            INSERT INTO GroupTag(email_tagger, owner_email, fg_name, item_id, num_approval) \
            VALUES(%s, %s, %s, %s, 0);\
            '
            parameter = (email_tagger, owner_email, fg_name, item_id)
            query(sql, parameter)

            # insert group tag invitation for each group member
            sql = '\
            SELECT email \
            FROM Belong \
            WHERE owner_email = %s AND fg_name = %s;\
            '
            parameter = (owner_email, fg_name)
            member_list = query(sql, parameter)
            for member in member_list:
                sql = '\
                INSERT INTO GroupTagPending(email_tagged, email_tagger, owner_email, fg_name, item_id) \
                VALUES(%s, %s, %s, %s, %s);\
                '
                parameter = (member['email'], email_tagger, owner_email, fg_name, item_id)
                query(sql, parameter)
            msg = "Tag Successfully Posted, waiting for group members' approval."
            response = SuccessResponse({"msg": msg})
        else:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 9, "errormsg": "Group not found"})
    return jsonify(response.__dict__)


@api.route('/grouptag_count', methods=['GET'])
def grouptag_count():
    try:
        email = session['email']  # authenticate login
        sql = '\
        SELECT COUNT(*) AS grouptag_number \
        FROM GroupTagPending \
        WHERE email_tagged = %s AND status IS NULL;\
        '
        parameter = (email)
        data = query(sql, parameter)
        response = SuccessResponse(data[0])
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/pending_grouptag', methods=['GET'])
def pending_grouptag():
    try:
        email = session['email']  # authenticate login
        sql = '\
        SELECT * \
        FROM GroupTagPending NATURAL JOIN ContentItem \
        WHERE email_tagged = %s AND status IS NULL \
        ORDER BY tagtime DESC;\
        '
        parameter = (email)
        data = query(sql, parameter)
        response = SuccessResponse({"grouptagList": data})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    return jsonify(response.__dict__)


@api.route('/grouptag', methods=['PATCH'])
def grouptag_patch():
    try:
        email = session['email']
        status = request.form['status']
        email_tagged = request.form['email_tagged']
        email_tagger = request.form['email_tagger']
        item_id = request.form['item_id']
        fg_name = request.form['fg_name']
        owner_email = request.form['owner_email']
        if email != email_tagged:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)
        if is_request_exist(email_tagged, email_tagger, owner_email, fg_name, item_id):
            parameter = (email_tagged, email_tagger, owner_email, fg_name, item_id)
            sql = '\
            DELETE FROM GroupTagPending \
            WHERE email_tagged = %s AND email_tagger = %s AND owner_email = %s AND fg_name = %s AND item_id = %s;\
            '
            query(sql, parameter)
        else:
            response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
            return jsonify(response.__dict__)

        if status == "1":
            # plus one
            sql = '\
            UPDATE GroupTag \
            SET num_approval = num_approval + 1 \
            WHERE email_tagger = %s AND owner_email = %s AND fg_name = %s AND item_id = %s;\
            '
            parameter = (email_tagger, owner_email, fg_name, item_id)
            query(sql, parameter)
        elif status == "0":
            # veto
            sql = '\
            UPDATE GroupTag \
            SET veto = 1 \
            WHERE email_tagger = %s AND owner_email = %s AND fg_name = %s AND item_id = %s;\
            '
            parameter = (email_tagger, owner_email, fg_name, item_id)
            query(sql, parameter)
        else:
            abort(400)
        # delete a processed request
        response = SuccessResponse({"msg": "Successfully updated"})
    except KeyError:
        response = ErrorResponse({"code": 3, "errormsg": "session error"})
    except pymysql.err.IntegrityError:
        response = ErrorResponse({"code": 5, "errormsg": "invalid parameter, please check"})
    return jsonify(response.__dict__)


@api.route('/grouptag', methods=['GET'])
def get_grouptag():
    item_id = request.args['item_id']
    try:
        email = session['email']
    except KeyError:
        email = 'guest'
    if is_visible(item_id, email):
        sql = '\
        SELECT email_tagger, owner_email, fg_name \
        FROM GroupTag AS g \
        WHERE item_id = %s AND veto != 1 AND num_approval >= (SELECT count(*) FROM Belong WHERE owner_email =' \
              ' g.owner_email AND fg_name = g.fg_name) \
        ORDER BY tagtime DESC;\
        '
        parameter = (item_id)
        data = query(sql, parameter)
        response = SuccessResponse({"GrouptagList": data})
    else:
        response = ErrorResponse({"code": 4, "errormsg": "Permission Denied"})
    return jsonify(response.__dict__)


#############################
#        ITEM TYPES         #
#############################
@api.route('/typed_content', methods=['GET'])
def get_content_by_type():
    pass
