import os
from db import db
from app import app
from flask import redirect, render_template, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

# welcome page
@app.route("/")
def index():
    return render_template("index.html")

# leaving the quizzes
@app.route("/end")
def end():
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
    password = request.form["password1"]
    password2 = request.form["password2"]
    if password != password2:
        return render_template("error.html", message = 'Salasanat eroavat')
    if password2 == '':
        return render_template("error.html", message = 'Salasanat eroavat')
    role =  request.form["role"]
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (name, password, role) VALUES (:name, :password, :role)")
    db.session.execute(sql, {"name":name,"password":hash_value,"role":role})
    db.session.commit()
    return redirect("/")

# quizzes are listed depending of the role
@app.route("/quiz", methods=["GET","POST"])
def quiz():
    if request.method == "GET":
        creator_id = session["user_id"] 
        sql = text("SELECT id, name FROM quizzes WHERE visible=1 AND creator_id=:creator_id")
        result = db.session.execute(sql, {"creator_id":creator_id})
        quizzes = result.fetchall()
        if session["user_role"] == 1:
            sql = text("SELECT id, name FROM quizzes WHERE visible=1")
            result = db.session.execute(sql)
            quizzes = result.fetchall()
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT id, password, role FROM users WHERE name=:name")
        result = db.session.execute(sql, {"name":name})
        user = result.fetchone()
        if not check_password_hash(user[1], password):
            return render_template("error.html", message = 'Tunnus tai salasana virheellinen')
        session["user_id"] = user[0]
        session["user_name"] = name
        session["user_role"] = user[2]
        if user[2] == 2:
            creator_id = user[0]
            sql = text("SELECT id, name FROM quizzes WHERE visible=1 AND creator_id=:creator_id")
            result = db.session.execute(sql, {"creator_id":creator_id})
            quizzes = result.fetchall()
        else:
            sql = text("SELECT id, name FROM quizzes WHERE visible=1")
            result = db.session.execute(sql)
            quizzes = result.fetchall()
    return render_template("quiz.html", quizzes=quizzes)

# to be done
@app.route("/userstat")
def userstat():
    return render_template("userstat.html")

# template for quiz creation details
@app.route("/new_quiz")
def new_quiz():
    return render_template("create_quiz.html")

# new quiz and quiz questions will be created unless name of the quiz is empty or questions are empty
@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    name = request.form["new_quiz"]
    creator_id = session["user_id"]
    if name != "":
        sql = text("INSERT INTO quizzes (creator_id, name, visible) VALUES (:creator_id, :name, :visible) RETURNING id")
        result = db.session.execute(sql, {"creator_id":creator_id,"name":name,"visible":1})
        quiz_id = result.fetchone()[0]
        questions = request.form.getlist("question")
        for question in questions:
            if question != "":
                sql = text("INSERT INTO questions (quiz_id, question, qvisible) VALUES (:quiz_id, :question, :qvisible)")
                db.session.execute(sql, {"quiz_id":quiz_id,"question":question,"qvisible":1})
        db.session.commit()
    return redirect("/questions/" + str(quiz_id))

# will be checked if question has already at least one answer
@app.route("/answers/<int:id>")
def answers(id):
    quest_id = id
    sql = text("SELECT * FROM qanswers WHERE quest_id=:quest_id")
    result = db.session.execute(sql, {"quest_id":quest_id}).fetchone()
    if result:
        return render_template("error.html", message = 'Kysymykselle on jo vastaus')
    return render_template("answers.html", id=id)

#questions are listed for giving answers       
@app.route("/questions/<int:quiz_id>")
def questions(quiz_id):
    sql = text("SELECT id, question FROM questions WHERE quiz_id=:quiz_id")
    result = db.session.execute(sql, {"quiz_id":quiz_id})
    questions = result.fetchall()
    return render_template("questions.html", questions=questions, quiz_id=quiz_id)

# all answers to question will be updated unless the correct answer is empty
@app.route("/create_answer", methods=["POST"])
def create_answer():
    answer = request.form["correct"]
    quest_id = request.form["id"]
    id = quest_id
    sql = text("SELECT quiz_id FROM questions WHERE id=:id")
    quiz_id = db.session.execute(sql, {"id":id}).fetchone()[0]
    if answer != "":
        sql = text("INSERT INTO qanswers (answer, quest_id, correct) VALUES (:answer, :quest_id, :correct)")
        db.session.execute(sql, {"answer":answer,"quest_id":quest_id,"correct":1})
        wrongs = request.form.getlist("wrong")
        for wrong in wrongs:
            if wrong != "":
                answer = wrong
                sql = text("INSERT INTO qanswers (answer, quest_id, correct) VALUES (:answer, :quest_id, :correct)")
                db.session.execute(sql, {"answer":answer,"quest_id":quest_id,"correct":0})
        db.session.commit()            
    return redirect ("/questions/" + str(quiz_id))

# quiz will be deleted directly by clicking the link
@app.route("/del_quiz/<int:quiz_id>")
def del_quiz(quiz_id):
    id = quiz_id
    sql = text("UPDATE quizzes SET visible = 0 WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit() 
    return redirect ("/quiz")

@app.route("/attend/<int:id>")
def attend(id):
    quest_id = id
    sql = text("SELECT * FROM qanswers WHERE quest_id=:quest_id ORDER BY answer ASC")
    choices = db.session.execute(sql, {"quest_id":quest_id}).fetchall()
    sql = text("SELECT quiz_id FROM questions WHERE id=:id")
    quiz_id = db.session.execute(sql, {"id":id}).fetchone()[0]
    if len(choices) == 0:
        return render_template("error.html", message = 'Kysymyksellä ei ole vastausta!')
    return render_template("attend.html", choices=choices, quest_id=quest_id, count=len(choices), quiz_id=quiz_id)

#show whether the answer is correct and update attendee points only once
@app.route("/result", methods=["POST"])
def result():
    answer = request.form["answer"].strip()
    quest_id = request.form["quest_id"]
    sql = text("SELECT answer FROM qanswers WHERE quest_id=:quest_id AND correct=1")
    correct = db.session.execute(sql, {"quest_id":quest_id}).fetchone()[0]
    id = quest_id
    sql = text("SELECT quiz_id FROM questions WHERE id=:id")
    quiz_id = db.session.execute(sql, {"id":id}).fetchone()[0]
    if answer == correct:
        user_id = session["user_id"]
        sql = text("SELECT * FROM apoints WHERE user_id=:user_id AND quiz_id=:quiz_id AND quest_id=:quest_id")
        point = db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id, "quest_id":quest_id}).fetchone()
        if point:
            return render_template("error.html", message = 'Kysymyksen vastaukselle on jo annettu piste.')
        else:
            sql = text("INSERT INTO apoints (user_id, quiz_id, quest_id, points) VALUES (:user_id, :quiz_id, :quest_id, :points)")
            db.session.execute(sql,{"user_id":user_id, "quiz_id":quiz_id, "quest_id":quest_id,"points":1})
            db.session.commit() 
    return render_template("result.html", correct=correct, answer=answer, quest_id=quest_id, quiz_id=quiz_id)