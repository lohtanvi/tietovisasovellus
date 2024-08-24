import os
from db import db
from app import app
from flask import redirect, render_template, session, request, abort
from werkzeug.security import check_password_hash
import quizz
import users
import questanswer
import points


# welcome page
@app.route("/")
def index():
    return render_template("index.html")

# leaving the quizzes
@app.route("/end")
def end():
    user_stat = session.get("user_id", 0)
    if not user_stat:
        return render_template("index.html", message = 'Et ole kirjautunut.')  
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]
    return render_template("end.html")

#template for login details
@app.route("/login")
def login():
    return render_template("login.html")

#template for user creation details
@app.route("/newuser")
def newuser():
    return render_template("newuser.html")

#user and password creation
@app.route("/create_user", methods=["POST"])
def create_user():
    name = request.form["username"]
    result = users.get_users_data(name)
    if result:
        return render_template("newuser.html", message = 'Käyttäjätunnus on varattu. Valitse toinen käyttäjätunnus.')
    if len(name) < 1 or len(name) > 20:
        return render_template("newuser.html", message = 'Tunnuksessa tulee olla 1-20 merkkiä')
    password = request.form["password1"]
    password2 = request.form["password2"]
    if password != password2:
        return render_template("newuser.html", message = 'Salasanat eroavat')
    if password2 == '':
        return render_template("newuser.html", message = 'Salasana on tyhjä')
    role =  request.form["role"]
    if users.create_user(name,password,role):
        return render_template("/login.html", message = 'Uusi tunnus luotiin.')

# quizzes are listed depending of the role
@app.route("/quiz", methods=["GET","POST"])
def quiz():
    if request.method == "GET":
        user_stat = session.get("user_id", 0)
        if not user_stat:
            return render_template("index.html", message = 'Kirjaudu katsoaksesi tietovisoja.')  
        creator_id = session["user_id"] 
        quizzes = quizz.get_creator_quizzes(creator_id)
        notquizzes = quizz.get_creator_noquizzes(creator_id)
        if session["user_role"] == 1:
            quizzes = quizz.get_visible_quizzes()
            notquizzes = quizz.get_novisible_quizzes()
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        if name == '':
            return render_template("login.html", message = 'Käyttäjätunnusta ei annettu.')
        user = users.get_users_data(name)
        if not user:
            return render_template("login.html", message = 'Käyttäjätunnus ei täsmää.')
        if not check_password_hash(user[1], password):
            return render_template("login.html", message = 'Tunnus tai salasana virheellinen')
        session["user_id"] = user[0]
        session["user_name"] = name
        session["user_role"] = user[2]
        session["csrf_token"] = os.urandom(16).hex()
        if user[2] == 2:
            creator_id = user[0]
            quizzes = quizz.get_creator_quizzes(creator_id)
            notquizzes = quizz.get_creator_noquizzes(creator_id)
        else:
            quizzes = quizz.get_visible_quizzes()
            notquizzes = quizz.get_novisible_quizzes()
    return render_template("quiz.html", quizzes=quizzes, notquizzes=notquizzes)

#user_statistics
@app.route("/userstat")
def userstat():
    user_stat = session.get("user_id", 0)
    if not user_stat:
        return render_template("index.html", message = 'Kirjaudu katsoaksesi tilastot.')  
    user_id = session["user_id"]
    count1 = points.count_attendance(user_id)
    count2 = points.count_points(user_id)
    creator_id=user_id
    count3 = quizz.count_quizzes(creator_id)
    count4 = quizz.count_noquizzes(creator_id)
    return render_template("userstat.html", count1=count1, count2=count2, count3=count3, count4=count4)

# template for quiz creation details
@app.route("/new_quiz")
def new_quiz():
    return render_template("create_quiz.html")

# new quiz and quiz questions will be created unless name of the quiz is empty or questions are empty
@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["new_quiz"]
    if name == "":
        return render_template("create_quiz.html", message = 'Tietovisalla ei ole nimeä')
    creator_id = session["user_id"]
    if name != "":
        quiz_id = quizz.create_quiz_name(creator_id,name)
        questions = request.form.getlist("question")
        for question in questions:
            if question != "":
                questanswer.create_question(quiz_id,question)
    return redirect("/questions/" + str(quiz_id))

# will be checked if question has already at least one answer
@app.route("/answers/<int:id>")
def answers(id):
    quest_id = id
    result = questanswer.get_answers(quest_id)
    if result:
        return render_template("answers.html", id = id, message = 'Kysymykselle on jo vastaus')
    return render_template("answers.html", id=id)

#questions are listed for giving answers       
@app.route("/questions/<int:quiz_id>")
def questions(quiz_id):
    quiz_id=quiz_id
    questions = questanswer.get_questions(quiz_id)
    return render_template("questions.html", questions=questions, quiz_id=quiz_id)

# all answers to question will be updated unless the correct answer is empty
@app.route("/create_answer", methods=["POST"])
def create_answer():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    answer = request.form["correct"]
    quest_id = request.form["id"]
    id = quest_id
    quiz_id = questanswer.get_quiz_id(id)
    if answer != "":
        questanswer.create_answer(answer,quest_id)
        wrongs = request.form.getlist("wrong")
        for wrong in wrongs:
            if wrong != "":
                answer = wrong
                questanswer.create_answerchoice(answer,quest_id)         
    return redirect ("/questions/" + str(quiz_id))

# quiz will be deleted directly by clicking the link
@app.route("/del_quiz/<int:quiz_id>")
def del_quiz(quiz_id):
    id = quiz_id
    quizz.set_quiz_invisible(id)
    return redirect ("/quiz")

@app.route("/activate_quiz/<int:quiz_id>")
def activate_quiz(quiz_id):
    id = quiz_id
    quizz.set_quiz_visible(id)
    return redirect ("/quiz")

#attend the quiz by answering to questions
@app.route("/attend/<int:id>")
def attend(id):
    quest_id = id
    choices = questanswer.get_answerchoice(quest_id)
    quiz_id = questanswer.get_quiz_id(id)
    if len(choices) == 0:
        questions = questanswer.get_questions(quiz_id)
        return render_template("questions.html", questions=questions, quiz_id=quiz_id, message = 'Kysymyksen tekijä ei ole luonut kysymykselle vastausta!')
    return render_template("attend.html", choices=choices, quest_id=quest_id, count=len(choices), quiz_id=quiz_id)

#show whether the answer is correct and update attendee points only once
@app.route("/result", methods=["POST"])
def result():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    answer = request.form["answer"].strip()
    quest_id = request.form["quest_id"]
    correct = questanswer.get_correct_answer(quest_id)
    id = quest_id
    quiz_id = questanswer.get_quiz_id(id)
    if answer == correct:
        user_id = session["user_id"]
        point = points.get_point(user_id,quiz_id,quest_id)
        if point:
            return render_template ("result.html", correct=correct, answer=answer, quest_id=quest_id, quiz_id=quiz_id, message = 'Kysymyksen vastaukselle on jo annettu piste. Et voi saada enempää pisteitä')
        else:
            points.give_point(user_id,quiz_id,quest_id)
    return render_template("result.html", correct=correct, answer=answer, quest_id=quest_id, quiz_id=quiz_id)