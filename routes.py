import os
from db import db
from app import app
from flask import redirect, render_template, session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/end")
def end():
    return render_template("end.html")

@app.route("/newuser")
def newuser():
    return render_template("newuser.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    name = request.form["name"]
    password = request.form["password"]
    role =  request.form["role"]
#  TO DO password checks and security - password2 = request.form["password2"]
 #       hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (name, password, role) VALUES (:name, :password, :role)")
    db.session.execute(sql, {"name":name,"password":password,"role":role})
    db.session.commit()
    return redirect("/")

@app.route("/quiz", methods=["POST"])
def quiz():
    result = db.session.execute(text("SELECT id, name FROM quizzes WHERE visible=1"))
    quizzes = result.fetchall()
    return render_template("quiz.html", name=request.form["username"], quizzes=quizzes)

@app.route("/userstat")
def userstat():
    return render_template("userstat.html")

@app.route("/new_quiz")
def new_quiz():
    return render_template("create_quiz.html")

@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    name = request.form["new_quiz"]
#    creator_id = to be implemented 
    sql = text("INSERT INTO quizzes (creator_id, name, visible) VALUES (:creator_id, :name, :visible) RETURNING id")
    result = db.session.execute(sql, {"creator_id":2,"name":name,"visible":1})
    quiz_id = result.fetchone()[0]
    questions = request.form.getlist("question")
    for question in questions:
        if question != "":
            sql = text("INSERT INTO questions (quiz_id, question, qvisible) VALUES (:quiz_id, :question, :qvisible)")
            db.session.execute(sql, {"quiz_id":quiz_id,"question":question,"qvisible":1})
    db.session.commit()
    return redirect("/answers")

@app.route("/answers")
def answers():
    result = db.session.execute(text("SELECT id, question FROM questions WHERE quiz_id=7")) 
# quiz_id to be implemented
    questions = result.fetchall()
    return render_template("answers.html", questions=questions)
