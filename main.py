from flask import Flask, render_template, request, redirect
import function
import datetime


app = Flask(__name__)


@app.route("/")
def show_list():
    '''Renders the Questions table'''
    question_table = function.sql_query_get("""SELECT * FROM question ORDER BY id LIMIT 5;""")
    return render_template('list.html', question_table=question_table)


@app.route("/list", methods=['GET', 'POST'])
def sort_question():
    '''Sorts questions list'''
    sorted_by_criteria = function.sort_query()
    return render_template('list.html', question_table=sorted_by_criteria)


@app.route("/search", methods=['GET', 'POST'])
def search_function():
    '''Renders the Questions table'''
    question_table = function.search_query()
    return render_template('list.html', question_table=question_table)


@app.route("/all")
def show_list_latest():
    '''Renders the Questions table'''
    question_table = function.sql_query_get("""SELECT * FROM question;""")
    return render_template('list.html', question_table=question_table)


@app.route("/question/<question_id>")
def question_details(question_id):
    '''Renders question_details.html with the details of a given question'''
    question_table = function.select_query('*', 'question', 'id', question_id)
    answer_table = function.select_query('*', 'answer', 'question_id', question_id)
    question_comment_table = function.select_query('*', 'comment', 'question_id', question_id)
    answer_comment_query = ("SELECT comment.id,comment.question_id,comment.answer_id,comment.message,comment.submission_time,comment.edited_count FROM comment LEFT JOIN answer ON comment.answer_id=answer.id WHERE answer.question_id={};".format(question_id))
    answer_comment_table = function.sql_query_get(str(answer_comment_query))
    tag_query = ("SELECT  question_tag.question_id, tag.id, tag.name FROM question_tag INNER JOIN tag ON question_tag.tag_id=tag.id WHERE question_id = {};".format(question_id))
    tag_table = function.sql_query_get(str(tag_query))
    function.update_view_count_query(question_id)
    return render_template("question_details.html",
                           question=question_table[0],
                           answers=answer_table,
                           comments=question_comment_table,
                           answer_comment_table=answer_comment_table,
                           question_id=int(question_id),
                           tag_table=tag_table)


@app.route('/newquestion', methods=['GET', 'POST'])
def new_question():
    '''Renders question.html to get a new question,  then inserts it into the database
    \nRedirects to the questions list page'''
    if request.method == 'GET':
        select_user_list = function.select_user()

        return render_template("question.html", user_list=select_user_list)

    if request.method == "POST":
        function.add_new_question()
        return redirect("./")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    '''Deletes a given question, then redirects to main page'''
    if request.method == 'POST':
        function.delete_query('question_tag', 'question_id', question_id)
        answer_comment_delete = (
            "DELETE FROM comment WHERE answer_id IN(SELECT answer_id FROM answer WHERE question_id={});".format(question_id))
        function.sql_query_post(str(answer_comment_delete))
        function.delete_query('answer', 'question_id', question_id)
        function.delete_query('comment', 'question_id', question_id)
        function.delete_query('question', 'id', question_id)
        return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    '''Renders answer.html to get a new answer, then inserts it into the database
    \nRedirects to the given question's detail page'''
    if request.method == 'GET':
        select_user_list = function.select_user()
        return render_template("answer.html", question_id=question_id, user_list=select_user_list)

    if request.method == 'POST':
        function.add_new_answer(question_id)
        return redirect("/question/{}".format(question_id))


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    '''Deletes given answer, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    function.delete_query('comment', 'answer_id', answer_id)
    function.delete_query('answer', 'id', answer_id)
    return redirect("/question/{}".format(question_id))


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    '''Renders question.html to edit a given question, then updates the question in the database file
    \n Redirects to the question's detail page'''
    if request.method == 'GET':
        edit_question_row = function.select_query('*', 'question', 'id', question_id)
        return render_template("question.html", question_id=question_id, message=edit_question_row[0][5], title=edit_question_row[0][4])

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


@app.route('/answer/<answer_id>/vote-up', methods=['POST', 'GET'])
def answer_vote_up(answer_id):
    '''Increases the vote count of the given answer'''
    question_id = request.form['questionid']
    function.vote_update_sql_query('answer', answer_id, 'up')
    return redirect("./question/{}".format(question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST', 'GET'])
def answer_vote_down(answer_id):
    '''Decreases the vote count of the given answer'''
    question_id = request.form['questionid']
    function.vote_update_sql_query('answer', answer_id, 'down')
    return redirect("./question/{}".format(question_id))


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_new_question_comment(question_id):
    '''adds new comment to given question'''
    if request.method == 'GET':
        return render_template("comment.html", question_id=question_id)

    if request.method == 'POST':
        function.add_new_comment(question_id, 'question_id')
        return redirect("/question/{}".format(question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_new__answer_comment(answer_id):
    '''adds new comment to given answer'''
    if request.method == 'GET':
        return render_template("comment.html", answer_id=answer_id)

    if request.method == 'POST':
        function.add_new_comment(answer_id, 'answer_id')
        question_id = function.select_query('question_id', 'answer', 'id', answer_id)
        return redirect("/question/{}".format(question_id[0][0]))


@app.route('/comment/<comment_id>/delete', methods=['GET', 'POST'])
def delete_comment(comment_id):
    '''Deletes given comment, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    function.delete_query('comment', 'id', comment_id)
    return redirect("/question/{}".format(question_id))


@app.route('/question/<question_id>/new-tag', methods=['GET'])
def new_tag(question_id):
    '''renders new_tag.html to add or select a new tag for the question'''
    existing_tags = function.sql_query_get("SELECT name FROM tag;")
    return render_template("new_tag.html", existing_tags=existing_tags, question_id=question_id)


@app.route('/question/<question_id>/add-new-tag', methods=['GET', 'POST'])
def add_new_tag(question_id):
    '''Adds new tag to the question'''
    tag_to_add = request.form['tag-text']
    tag_insert_query = """INSERT INTO tag (name) VALUES ('{}');""".format(tag_to_add)
    function.sql_query_post(tag_insert_query)
    tag_id = function.select_query("id", "tag", "name", tag_to_add)
    question_tag_insert_query = """INSERT INTO question_tag (question_id,tag_id) VALUES ('{}','{}');""".format(
        question_id, int(tag_id[0][0]))
    try:
        function.sql_query_post(question_tag_insert_query)
    except:
        return redirect('/question/{}'.format(question_id))
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<question_id>/submit-new-tag/<tag_name>', methods=['GET', 'POST'])
def submit_new_tag(question_id, tag_name):
    '''Adds a new tag to the given question'''
    tag_id = function.select_query("id", "tag", "name", tag_name)
    question_tag_insert_query = """INSERT INTO question_tag (question_id,tag_id) VALUES ('{}','{}');""".format(
        question_id, tag_id[0][0])
    try:
        function.sql_query_post(question_tag_insert_query)
    except:
        return redirect('/question/{}'.format(question_id))
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<question_id>/tag/<tag_id>/delete', methods=['GET', 'POST'])
def delete_tag(question_id, tag_id):
    '''Deletes given tags, then redirects to the question's detail page'''
    sql_to_delete = ("DELETE FROM  question_tag WHERE tag_id={} AND question_id={};".format(tag_id, question_id))
    function.sql_query_post(str(sql_to_delete))
    return redirect("/question/{}".format(question_id))


if __name__ == '__main__':
    app.run(debug=True)
