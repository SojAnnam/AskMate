from flask import Flask, render_template, request, redirect
import function
import datetime


app = Flask(__name__)


@app.route("/")
def show_list():
    '''Renders the Questions table'''
    header_row = ["ID",
                  "Title",
                  "Message",
                  "Views",
                  "Votes",
                  "",
                  "Time",
                  "Delete"
                  ]
    question_table = function.sql_query_get("""SELECT * FROM question;""")
    return render_template('list.html', question_table=question_table)


@app.route("/list", methods=['GET', 'POST'])
def sort_question():
    for key in request.args:
        criteria = key
        order = request.args.get(key)
    query = "SELECT * FROM question ORDER BY {} {};".format(criteria, order)
    sorted_question = function.sql_query_get(query)
    return render_template('list.html', question_table=sorted_question)


@app.route("/search", methods=['GET', 'POST'])
def search_question():
    '''Renders the Questions table'''
    header_row = ["ID",
                  "Title",
                  "Message",
                  "Views",
                  "Votes",
                  "",
                  "Time",
                  "Delete"
                  ]
    search_parameter = request.form['search']
    query = """SELECT DISTINCT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image
    FROM question LEFT JOIN answer ON question.id=answer.question_id
    WHERE question.title LIKE '%{}%'
    OR question.message LIKE '%{}%'
    OR answer.message LIKE '%{}%';""".format(search_parameter, search_parameter, search_parameter)
    question_table = function.sql_query_get(str(query))
    return render_template('list.html', question_table=question_table, header_row=header_row)


@app.route("/latest")
def show_list_latest():
    '''Renders the Questions table'''
    header_row = ["ID",
                  "Title",
                  "Message",
                  "Views",
                  "Votes",
                  "",
                  "Time",
                  "Delete"
                  ]
    question_table = function.sql_query_get("""SELECT * FROM question LIMIT 5;""")
    return render_template('list.html', question_table=question_table, header_row=header_row)


@app.route("/question/<question_id>")
def question_details(question_id):
    '''Renders question_details.html with the details of a given question'''
    question_query = ("SELECT * FROM question WHERE id={};".format(question_id))
    question_table = function.sql_query_get(question_query)
    answer_query = ("SELECT * FROM answer WHERE question_id = {};".format(question_id))
    answer_table = function.sql_query_get(str(answer_query))
    comment_query = ("SELECT * FROM comment WHERE question_id = {};".format(question_id))
    comment_table = function.sql_query_get(str(comment_query))
    return render_template("question_details.html",
                           question=question_table[0],
                           answers=answer_table,
                           comments=comment_table,
                           question_id=int(question_id))


@app.route('/newquestion', methods=['GET', 'POST'])
def add_new_question():
    '''Renders question.html to get a new question, then writes that out to the csv file
    \nRedirects to the questions list page'''
    if request.method == 'GET':
        return render_template("question.html")

    if request.method == "POST":
        time = datetime.datetime.now()
        view_number = '0'
        vote_number = '0'
        title = request.form["title"]
        message = request.form["message"]
        sql_to_insert = ("INSERT INTO question (submission_time,view_number,vote_number,title,message) VALUES ('{}','{}','{}','{}','{}');".format(
            time, view_number, vote_number, title, message))
        function.sql_query_post(str(sql_to_insert))
        return redirect("./")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    '''Deletes a given question, then redirects to "./list"'''
    if request.method == 'POST':
        sql_to_delete_question_tag = ("DELETE FROM question_tag WHERE question_id={};".format(question_id))
        sql_to_delete_answer = ("DELETE FROM  answer WHERE question_id={};".format(question_id))
        sql_to_delete_comment = ("DELETE FROM comment WHERE question_id={};".format(question_id))
        sql_to_delete_question = ("DELETE FROM question WHERE id={};".format(question_id))
        function.sql_query_post(str(sql_to_delete_question_tag))
        function.sql_query_post(str(sql_to_delete_answer))
        function.sql_query_post(str(sql_to_delete_comment))
        function.sql_query_post(str(sql_to_delete_question))
        return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    '''Renders answer.html to get a new answer, then writes that out to a csv file
    \nRedirects to the given question's detail page'''
    if request.method == 'GET':
        return render_template("answer.html", question_id=question_id)

    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        vote_number = '0'
        answer_message = request.form["newanswer"]
        sql_to_insert_answer = ("INSERT INTO answer (submission_time,vote_number,question_id,message) VALUES ('{}','{}','{}','{}');".format(
            submission_time, vote_number, question_id, answer_message))
        function.sql_query_post(str(sql_to_insert_answer))
        return redirect("/question/{}".format(question_id))


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    '''Deletes given answer, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    sql_to_delete_comment = ("DELETE FROM comment WHERE answer_id={};".format(answer_id))
    sql_to_delete_answer = ("DELETE FROM  answer WHERE id={};".format(answer_id))
    function.sql_query_post(str(sql_to_delete_comment))
    function.sql_query_post(str(sql_to_delete_answer))
    return redirect("/question/{}".format(question_id))


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    '''Renders question.html to edit a given question, then updates the question in the csv file
    \n Redirects to the question's detail page'''
    if request.method == 'GET':
        question_query = ("SELECT * FROM question WHERE id={};".format(question_id))
        edit_question_row = function.sql_query_get(question_query)
        print(edit_question_row)
        return render_template("question.html", question_id=question_id, message=edit_question_row[0][5], title=edit_question_row[0][4])

    if request.method == 'POST':
        question_title = request.form['title']
        question_message = request.form['message']
        sql_to_edit_question = ("UPDATE question SET title= '{}', message='{}' WHERE id= {};".format(
            question_title, question_message, question_id))
        function.sql_query_post(str(sql_to_edit_question))
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
def add_new_comment(question_id):
    if request.method == 'GET':
        return render_template("comment.html", question_id=question_id)

    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        edit_number = '0'
        comment_message = request.form["newcomment"]
        sql_to_insert_comment = ("INSERT INTO comment (question_id,message,submission_time,edited_count) VALUES ('{}','{}','{}','{}');".format(
            question_id, comment_message, submission_time, edit_number))
        function.sql_query_post(str(sql_to_insert_comment))
        return redirect("/question/{}".format(question_id))


if __name__ == '__main__':
    app.run(debug=True)
