from flask import Flask, render_template, request, redirect
import function
import datetime


app = Flask(__name__)


@app.route("/")
def show_list():
    '''Renders the Questions table'''
    question_table = function.sql_query_get("""SELECT * FROM question;""")
    return render_template('list.html', question_table=question_table)


@app.route("/list", methods=['GET', 'POST'])
def sort_question():
    sorted_by_criteria = function.sort_query()
    return render_template('list.html', question_table=sorted_by_criteria)


@app.route("/search", methods=['GET', 'POST'])
def search_function():
    '''Renders the Questions table'''
    question_table = function.search_query()
    return render_template('list.html', question_table=question_table)


@app.route("/latest")
def show_list_latest():
    '''Renders the Questions table'''
    question_table = function.sql_query_get("""SELECT * FROM question LIMIT 5;""")
    return render_template('list.html', question_table=question_table)


@app.route("/question/<question_id>")
def question_details(question_id):
    '''Renders question_details.html with the details of a given question'''
    question_table = function.select__query('question', 'id', question_id)
    answer_table = function.select__query('answer', 'question_id', question_id)
    question_comment_table = function.select__query('comment', 'question_id', question_id)
    answer_comment_query = ("SELECT comment.id,comment.question_id,comment.answer_id,comment.message,comment.submission_time,comment.edited_count FROM comment LEFT JOIN answer ON comment.answer_id=answer.id WHERE answer.question_id={};".format(question_id))
    answer_comment_table = function.sql_query_get(str(answer_comment_query))
    return render_template("question_details.html",
                           question=question_table[0],
                           answers=answer_table,
                           comments=question_comment_table,
                           answer_comment_table=answer_comment_table,
                           question_id=int(question_id))


@app.route('/newquestion', methods=['GET', 'POST'])
def new_question():
    '''Renders question.html to get a new question, then writes that out to the csv file
    \nRedirects to the questions list page'''
    if request.method == 'GET':
        return render_template("question.html")

    if request.method == "POST":
        function.add_new_question()
        return redirect("./")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    '''Deletes a given question, then redirects to "./list"'''
    if request.method == 'POST':
        function.delete_query('question_tag', 'question_id', question_id)
        function.delete_query('answer', 'question_id', question_id)
        function.delete_query('comment', 'question_id', question_id)
        function.delete_query('question', 'id', question_id)
        return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    '''Renders answer.html to get a new answer, then writes that out to a csv file
    \nRedirects to the given question's detail page'''
    if request.method == 'GET':
        return render_template("answer.html", question_id=question_id)

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
    '''Renders question.html to edit a given question, then updates the question in the csv file
    \n Redirects to the question's detail page'''
    if request.method == 'GET':
        edit_question_row = function.select_query('question', 'id', question_id)
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
    if request.method == 'GET':
        return render_template("comment.html", question_id=question_id)

    if request.method == 'POST':
        function.add_new_comment(question_id, 'question_id')
        return redirect("/question/{}".format(question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_new__answer_comment(answer_id):
    if request.method == 'GET':
        return render_template("comment.html", answer_id=answer_id)

    if request.method == 'POST':
        function.add_new_comment(answer_id, 'answer_id')
        question_id_query = ("SELECT question_id FROM answer WHERE id={};".format(answer_id))
        question_id = function.sql_query_get(question_id_query)
        return redirect("/question/{}".format(question_id[0][0]))


@app.route('/comment/<comment_id>/delete', methods=['GET', 'POST'])
def delete_comment(comment_id):
    '''Deletes given answer, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    sql_to_delete_comment = ("DELETE FROM comment WHERE id={};".format(comment_id))
    function.sql_query_post(str(sql_to_delete_comment))
    return redirect("/question/{}".format(question_id))


if __name__ == '__main__':
    app.run(debug=True)
