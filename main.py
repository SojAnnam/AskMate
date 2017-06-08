from flask import Flask, render_template, request, redirect
import function
import datetime


app = Flask(__name__)


@app.route("/", methods=['GET'])
def show_list():
    '''Renders the Questions table'''
    question_table = function.sql_query_get("""SELECT * FROM question ORDER BY id LIMIT 5;""")
    return render_template('list.html', question_table=question_table)


@app.route("/list", methods=['GET', 'POST'])
def sort_question():
    '''Sorts questions list'''
    sorted_by_criteria = function.sort_query()
    return render_template('list.html', question_table=sorted_by_criteria)


@app.route("/search", methods=['POST'])
def search_function():
    '''Renders the Questions table'''
    question_table = function.search_query()
    return render_template('list.html', question_table=question_table)


@app.route("/all", methods=['GET'])
def show_list_latest():
    '''Renders the Questions table'''
    question_table = function.sql_query_get("""SELECT * FROM question;""")
    return render_template('list.html', question_table=question_table)


@app.route("/question/<question_id>", methods=['GET'])
def question_details(question_id):
    '''Renders question_details.html with the details of a given question'''
    question_table = function.question_select_query(question_id)
    answer_table = function.answer_select_query(question_id)
    question_comment_table = function.question_comment_select_query(question_id)
    answer_comment_table = function.answer_comment_select_query(question_id)
    tag_table = function.tag_select_query(question_id)
    function.update_view_count_query(question_id)
    return render_template("question_details.html",
                           question=question_table[0],
                           answers=answer_table,
                           comments=question_comment_table,
                           answer_comment_table=answer_comment_table,
                           question_id=int(question_id),
                           tag_table=tag_table)


@app.route('/newquestion', methods=['GET'])
def render_new_question():
    """Renders question.html to get a new question"""
    if request.method == 'GET':
        select_user_list = function.select_user()
        return render_template("question.html", user_list=select_user_list)


@app.route('/newquestion', methods=['POST'])
def new_question():
    """Inserts it into the database then Redirects to the questions list page"""
    if request.method == "POST":
        function.add_new_question()
        return redirect("./")


@app.route('/question/<question_id>/delete', methods=['POST'])
def delete_question(question_id):
    '''Deletes a given question, then redirects to main page'''
    if request.method == 'POST':
        function.delete_query('question_tag', 'question_id', question_id)
        function.delete_answer_comment_query(question_id)
        function.delete_query('answer', 'question_id', question_id)
        function.delete_query('comment', 'question_id', question_id)
        function.delete_query('question', 'id', question_id)
        return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=['GET'])
def render_new_answer(question_id):
    '''Renders answer.html to get a new answer'''
    if request.method == 'GET':
        select_user_list = function.select_user()
        return render_template("answer.html", question_id=question_id, user_list=select_user_list)


@app.route("/question/<question_id>/new-answer", methods=['POST'])
def new_answer(question_id):
    '''Inserts it into the database then Redirects to the given question's detail page'''
    if request.method == 'POST':
        function.add_new_answer(question_id)
        return redirect("/question/{}".format(question_id))


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    '''Deletes given answer, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    function.delete_query('comment', 'answer_id', answer_id)
    function.delete_query('answer', 'id', answer_id)
    return redirect("/question/{}".format(question_id))


@app.route("/question/<question_id>/edit", methods=['GET'])
def render_edit_question(question_id):
    """Renders question.html to edit a given question"""
    if request.method == 'GET':
        edit_question_row = function.select_query('*', 'question', 'id', question_id)
        return render_template("question.html", question_id=question_id, message=edit_question_row[0][5], title=edit_question_row[0][4])


@app.route("/question/<question_id>/edit", methods=['POST'])
def edit_question(question_id):
    """Updates the question in the database file then Redirects to the question's detail page"""
    if request.method == 'POST':
        function.edit_question_query(question_id)
        return redirect("/question/{}".format(question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST', 'GET'])
def question_vote_up(question_id):
    '''Increases the vote count of the given question'''
    function.vote_update_sql_query('question', question_id, 'up')
    return redirect('./')


@app.route('/question/<question_id>/vote-down', methods=['POST', 'GET'])
def question_vote_down(question_id):
    '''Decreases the vote count of the given question'''
    function.vote_update_sql_query('question', question_id, 'down')
    return redirect('./')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def answer_vote_up(answer_id):
    '''Increases the vote count of the given answer'''
    question_id = request.form['questionid']
    function.vote_update_sql_query('answer', answer_id, 'up')
    return redirect("./question/{}".format(question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def answer_vote_down(answer_id):
    '''Decreases the vote count of the given answer'''
    question_id = request.form['questionid']
    function.vote_update_sql_query('answer', answer_id, 'down')
    return redirect("./question/{}".format(question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET'])
def render_add_new_question_comment(question_id):
    '''Renders comment.html to adds new comment to given question'''
    if request.method == 'GET':
        select_user_list = function.select_user()
        return render_template("comment.html", question_id=question_id, user_list=select_user_list)


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def add_new_question_comment(question_id):
    """Add comment to a given question then render question_details.html"""
    if request.method == 'POST':
        function.add_new_comment(question_id, 'question_id')
        return redirect("/question/{}".format(question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['GET'])
def render_add_new__answer_comment(answer_id):
    '''Renders comment.html to adds new comment to given answer'''
    if request.method == 'GET':
        select_user_list = function.select_user()
        return render_template("comment.html", answer_id=answer_id, user_list=select_user_list)


@app.route('/answer/<answer_id>/new-comment', methods=['POST'])
def add_new__answer_comment(answer_id):
    """Add comment to a given question then render question_details.html"""
    if request.method == 'POST':
        function.add_new_comment(answer_id, 'answer_id')
        question_id = function.select_query('question_id', 'answer', 'id', answer_id)
        return redirect("/question/{}".format(question_id[0][0]))


@app.route('/comment/<comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    '''Deletes given comment, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    function.delete_query('comment', 'id', comment_id)
    return redirect("/question/{}".format(question_id))


@app.route('/question/<question_id>/new-tag', methods=['GET'])
def new_tag(question_id):
    '''Renders new_tag.html to add or select a new tag for the question'''
    existing_tags = function.sql_query_get("SELECT name FROM tag;")
    return render_template("new_tag.html", existing_tags=existing_tags, question_id=question_id)


@app.route('/question/<question_id>/add-new-tag', methods=['POST'])
def add_new_tag(question_id):
    '''Adds new tag to the question'''
    tag_to_add = request.form['tag-text']
    tag_insert_query = """INSERT INTO tag (name) VALUES ('{}');""".format(tag_to_add)
    function.sql_query_post(tag_insert_query)
    tag_id = function.select_query("id", "tag", "name", tag_to_add)
    try:
        function.question_tag_insert_query(question_id, (tag_id[0][0]))
    except:
        return redirect('/question/{}'.format(question_id))
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<question_id>/submit-new-tag/<tag_name>', methods=['GET', 'POST'])
def submit_new_tag(question_id, tag_name):
    '''Adds a new tag to the given question'''
    tag_id = function.select_query("id", "tag", "name", tag_name)
    try:
        function.question_tag_insert_query(question_id, (tag_id[0][0]))
    except:
        return redirect('/question/{}'.format(question_id))
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<question_id>/tag/<tag_id>/delete', methods=['POST'])
def delete_tag(question_id, tag_id):
    '''Deletes given tags, then redirects to the question's detail page'''
    sql_to_delete = ("DELETE FROM  question_tag WHERE tag_id={} AND question_id={};".format(tag_id, question_id))
    function.sql_query_post(str(sql_to_delete))
    return redirect("/question/{}".format(question_id))


@app.route("/user/<user_id>")
def user_activities(user_id):
    '''Renders user_activity.html with all the activities of a given user'''
    user_name_query = ("""SELECT username
                          FROM users
                          WHERE id={};""".format(user_id))
    user_name_result = function.sql_query_get(user_name_query)

    questions_header = ["Question"]
    user_questions_query = ("""SELECT question.user_id, question.id, question.title
                               FROM question
                               WHERE question.user_id={};""".format(user_id))
    user_questions_result = function.sql_query_get(user_questions_query)

    answers_header = ["Question", "Answer"]
    user_answers_query = ("""SELECT answer.user_id, question.id, question.title, answer.message
                             FROM question
                             INNER JOIN answer
                             ON question.id = answer.question_id
                             WHERE answer.user_id={};""".format(user_id))
    user_answers_result = function.sql_query_get(user_answers_query)

    comments_header = ["Question", "Answer", "Comment"]
    user_question_comments_query = ("""SELECT question.id, question.title, comment.id, comment.message, comment.user_id
                                       FROM comment INNER JOIN question ON question.id=comment.question_id
                                       WHERE comment.user_id={};""".format(user_id))
    user_question_comments_result = function.sql_query_get(user_question_comments_query)

    user_answer_comments_query = ("""SELECT question.id, question.title, answer.id, answer.message, comment.id, comment.message, comment.user_id
                                     FROM ((comment LEFT JOIN answer ON answer.id=comment.answer_id)
                                     INNER JOIN question ON question.id=answer.question_id)
                                     WHERE comment.user_id={};""".format(user_id))
    user_answer_comments_result = function.sql_query_get(user_answer_comments_query)

    return render_template("user_activity.html",
                           user_name=user_name_result[0][0],
                           questions_header=questions_header,
                           user_questions=user_questions_result,
                           answers_header=answers_header,
                           user_answers=user_answers_result,
                           comments_header=comments_header,
                           user_question_comments=user_question_comments_result,
                           user_answer_comments=user_answer_comments_result,)


@app.route('/registration/register-user', methods=['POST'])
def register_user():
    user_name = request.form['username']
    date = datetime.datetime.now()
    register_user_query = """INSERT INTO users
                            (username, date)
                            VALUES ('{}','{}')""".format(user_name, date)
    function.sql_query_post(str(register_user_query))
    return redirect("./")


@app.route('/registration')
def user_registration():
    return render_template("user_registration.html")


@app.route('/users')
def list_users():
    get_users_query = """SELECT * FROM users;"""
    users_list = function.sql_query_get(get_users_query)
    return render_template("user_list.html", users_list=users_list)


if __name__ == '__main__':
    app.run(debug=True)
