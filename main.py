from flask import Flask, render_template, request, redirect
import function
import time


app = Flask(__name__)


@app.route("/")
@app.route("/list")
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
    question_table = function.sql_query("""SELECT * FROM question;""")
    print("***************************")
    print(type(question_table))
    return render_template('list.html', question_table=question_table, header_row=header_row)


@app.route("/question/<question_id>")
def question_details(question_id):
    '''Renders question_details.html with the details of a given question'''

    return render_template("question_details.html",
                           question_title=question_title,
                           question_message=question_message,
                           question=question,
                           answers=answers,
                           question_id=question_id)


@app.route('/newquestion', methods=['GET', 'POST'])
def add_new_question():
    '''Renders question.html to get a new question, then writes that out to the csv file
    \nRedirects to the questions list page'''
    if request.method == 'GET':
        return render_template("question.html")

    if request.method == "POST":

        return redirect("./")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    '''Deletes a given question, then redirects to "./list"'''
    if request.method == 'POST':

        return redirect('./list')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    '''Renders answer.html to get a new answer, then writes that out to a csv file
    \nRedirects to the given question's detail page'''
    if request.method == 'GET':
        return render_template("answer.html", question_id=question_id)

    if request.method == 'POST':

        return redirect("/question/{}".format(question_id))


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    '''Renders question.html to edit a given question, then updates the question in the csv file
    \n Redirects to the question's detail page'''
    if request.method == 'GET':

        return render_template("question.html", question_id=question_id, message=question_message, title=question_title)

    if request.method == 'POST':

        return redirect("/question/{}".format(question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST', 'GET'])
def question_vote_up(question_id):
    '''Increases the vote count of the given question'''

    return redirect('./list')


@app.route('/question/<question_id>/vote-down', methods=['POST', 'GET'])
def question_vote_down(question_id):
    '''Decreases the vote count of the given question'''

    return redirect('./list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST', 'GET'])
def answer_vote_up(answer_id):
    '''Increases the vote count of the given answer'''
    return redirect("./question/{}".format(question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST', 'GET'])
def answer_vote_down(answer_id):
    '''Decreases the vote count of the given answer'''

    return redirect("./question/{}".format(question_id))


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    '''Deletes given answer, then redirects to the question's detail page'''
    return redirect("/question/{}".format(question_id))


if __name__ == '__main__':
    app.run(debug=True)
