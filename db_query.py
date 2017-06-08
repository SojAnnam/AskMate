import psycopg2
from flask import request
import datetime
import db_connection


def sort_query():
    for key in request.args:
        criteria = key
        order = request.args.get(key)
    query = "SELECT * FROM question ORDER BY {} {};".format(criteria, order)
    return db_connection.db_request(query)


def search_query():
    search_parameter = request.form['search']
    search_query = """SELECT DISTINCT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image
    FROM question LEFT JOIN answer ON question.id=answer.question_id
    WHERE question.title LIKE '%{}%'
    OR question.message LIKE '%{}%'
    OR answer.message LIKE '%{}%';""".format(search_parameter, search_parameter, search_parameter)
    return db_connection.db_request(str(search_query))


def add_new_question():
    """INSERT new question into question table"""
    submission_time = datetime.datetime.now()
    view_number = '0'
    vote_number = '0'
    question_title = request.form["title"]
    question_message = request.form["message"]
    question_user = request.form["user"]
    print(question_user)
    sql_to_insert = ("INSERT INTO question (submission_time,view_number,vote_number,title,message,user_id) VALUES ('{}','{}','{}','{}','{}','{}');".format(
        submission_time, view_number, vote_number, question_title, question_message, question_user))
    return db_connection.db_update(str(sql_to_insert))


def select_user():
    select_user_query = """SELECT id, username FROM users;"""
    return db_connection.db_request(select_user_query)


def add_new_answer(question_id):
    """Insert new answer into the answer table by question_id.Input parameter:question_id"""
    submission_time = datetime.datetime.now()
    vote_number = '0'
    answer_message = request.form["newanswer"]
    user_id = request.form["user"]
    sql_to_insert_answer = ("INSERT INTO answer (submission_time,vote_number,question_id,message,user_id) VALUES ('{}','{}','{}','{}','{}');".format(
        submission_time, vote_number, question_id, answer_message, user_id))
    db_connection.db_update(str(sql_to_insert_answer))


def select_query_where(column, table, criteria, condition):
    """SELECT row or rows from given table.
     Input parameters: table=given table, criteria= WHERE criteria, condition= WHERE condition"""
    question_query = ("SELECT {} FROM {} WHERE {}='{}';".format(column, table, criteria, condition))
    return db_connection.db_request(question_query)


def select_query(column, table):
    """SELECT row or rows from given table.Input parameters: column= column from given table table=given table"""
    select_table = ("SELECT {} FROM {};".format(column, table))
    return db_connection.db_request(select_table)


def select_order_by_query():
    question_table = ("""SELECT * FROM question ORDER BY id LIMIT 5;""")
    return db_connection.db_request(question_table)


def delete_query(table, criteria, condition):
    """DELETE row or rows from given table.
     Input parameters: table=given table, criteria= WHERE criteria, condition= WHERE condition"""
    sql_to_delete = ("DELETE FROM  {} WHERE {}={};".format(table, criteria, condition))
    return db_connection.db_update(str(sql_to_delete))


def edit_question_query(_id):
    """Update question table by question_id(input parameter: _id=WHERE condition)"""
    question_title = request.form['title']
    question_message = request.form['message']
    sql_to_edit_question = ("UPDATE question SET title= '{}', message='{}' WHERE id= {};".format(
        question_title, question_message, _id))
    db_connection.db_update(str(sql_to_edit_question))


def question_select_query(question_id):
    """Select question from question table and user from users table by question_id"""
    question_query = ("""SELECT question.id, question.submission_time,question.view_number,question.vote_number,question.title,question.message,users.username
                           FROM question
                           LEFT JOIN users ON question.user_id=users.id
                           WHERE question.id = {};""".format(question_id))
    return db_connection.db_request(str(question_query))


def answer_select_query(question_id):
    """Select answer from answer table and user from users table by question_id"""
    answer_query = ("""SELECT answer.id, answer.submission_time, answer.vote_number, answer.message, users.username
                         FROM answer
                         LEFT JOIN users ON answer.user_id = users.id
                         WHERE answer.question_id = {}; """.format(question_id))
    return db_connection.db_request(str(answer_query))


def question_comment_select_query(question_id):
    """Select question comment from comment table and user from users table by question_id"""
    question_comment_query = ("""SELECT comment.id, comment.message, comment.submission_time, users.username
                                FROM comment
                                LEFT JOIN users ON comment.user_id = users.id
                                WHERE comment.question_id = {}; """.format(question_id))
    return db_connection.db_request(str(question_comment_query))


def answer_comment_select_query(question_id):
    """Select answer comment from comment table and user from users table by question_id"""
    answer_comment_query = ("""SELECT comment.id, comment.answer_id, comment.message, comment.submission_time, users.username
                                 FROM comment
                                 LEFT JOIN users ON comment.user_id = users.id
                                 LEFT JOIN answer ON comment.answer_id = answer.id
                                 WHERE answer.question_id = {}; """.format(question_id))
    return db_connection.db_request(str(answer_comment_query))


def delete_answer_comment_query(question_id):
    answer_comment_delete = ("""DELETE FROM comment
                                WHERE answer_id
                                IN(SELECT answer_id FROM answer WHERE question_id={});""".format(question_id))
    return db_connection.db_update(str(answer_comment_delete))


def delete_tag_query(question_id, tag_id):
    sql_to_delete = ("DELETE FROM  question_tag WHERE tag_id={} AND question_id={};".format(tag_id, question_id))
    db_connection.db_update(str(sql_to_delete))


def question_tag_insert_query(question_id, tag_item):
    question_tag_insert = ("""INSERT INTO question_tag (question_id,tag_id)
                              VALUES ('{}','{}');""".format(question_id, int(tag_item)))
    return db_connection.db_update(question_tag_insert)


def insert_register_user(user_name, date):
    register_user_query = """INSERT INTO users
                            (username, date)
                            VALUES ('{}','{}')""".format(user_name, date)
    db_connection.db_update(str(register_user_query))


def tag_select_query(question_id):
    """Select tag from question_tag table by question_id"""
    tag_query = ("""SELECT  question_tag.question_id, tag.id, tag.name
                      FROM question_tag
                      INNER JOIN tag ON question_tag.tag_id=tag.id
                      WHERE question_id = {};""".format(question_id))
    return db_connection.db_request(str(tag_query))


def insert_tag_query(tag_to_add):
    tag_insert_query = """INSERT INTO tag (name) VALUES ('{}');""".format(tag_to_add)
    db_connection.db_update(tag_insert_query)


def add_new_comment(_id, id_type):
    """Insert a new comment into the comment table.
    Input parameters: _id(query value)= question_id or answer_id, id_type(sql coloumn)=question_id or answer_id"""
    submission_time = datetime.datetime.now()
    edit_number = '0'
    comment_message = request.form["newcomment"]
    user_id = request.form["user"]
    sql_to_insert_comment = ("INSERT INTO comment ({},message,submission_time,edited_count,user_id) VALUES ('{}','{}','{}','{}','{}');".format(
        id_type, _id, comment_message, submission_time, edit_number, user_id))
    db_connection.db_update(str(sql_to_insert_comment))


def vote_update_sql_query(table, _id, direction):
    """The function increase or decrease the vote_number.
    Input parameters:table=given table(answer or question), _id = answer_id or question_id,
    direction= 'up' or 'down'"""
    select_query = ("SELECT vote_number FROM {} WHERE id={};".format(table, _id))
    vote_number = db_connection.db_request(select_query)
    votes = int(vote_number[0][0])
    if direction == 'up':
        votes += 1
    elif direction == 'down':
        votes -= 1
    sql_to_edit_vote = ("UPDATE {} SET vote_number= {} WHERE id= {};".format(
        table, votes, _id))
    db_connection.db_update(str(sql_to_edit_vote))


def update_view_count_query(question_id):
    '''Increases the question's view counter by 1'''
    view_count = select_query_where("view_number", "question", "id", question_id)
    new_view_count = int(view_count[0][0]) + 1
    print(view_count)
    view_update_query = """UPDATE question SET view_number={} WHERE id={};""".format(new_view_count, question_id)
    db_connection.db_update(view_update_query)


def user_answers_query(user_id):
    """Select Users's Answers (and the relevant Questions)
    from the "answer" and "question" tables"""
    user_answers_query = ("""SELECT question.title, answer.message, question.id
                             FROM question
                             INNER JOIN answer
                             ON question.id = answer.question_id
                             WHERE answer.user_id={};""".format(user_id))
    return db_connection.db_request(user_answers_query)


def user_question_comments_query(user_id):
    """Select Users's Comments (and the relevant Questions)
    from the "comment" and "question" tables"""
    user_question_comments_query = ("""SELECT question.title, comment.message, question.id
                                       FROM comment INNER JOIN question ON question.id=comment.question_id
                                       WHERE comment.user_id={};""".format(user_id))
    return db_connection.db_request(user_question_comments_query)


def user_answer_comments_query(user_id):
    """Select Users's Comments (and the relevant Questions and Answers)
    from the "comment", "answer" and "question" tables"""
    user_answer_comments_query = ("""SELECT question.title, answer.message, comment.message, question.id
                                     FROM comment LEFT JOIN answer ON answer.id=comment.answer_id
                                     INNER JOIN question ON question.id=answer.question_id
                                     WHERE comment.user_id={};""".format(user_id))
    return db_connection.db_request(user_answer_comments_query)
