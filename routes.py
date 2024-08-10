import os
from db import db
from app import app
from flask import redirect, render_template, session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

#commnet

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/end")
def end():
    return render_template("end.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/newuser")
def newuser():
    return render_template("newuser.html")

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


@app.route("/quiz", methods=["POST"])
def quiz():
    name = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password, role FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not check_password_hash(user[1], password):
        return render_template("error.html", message = 'Tunnus tai salasana virheellinen')
    session["user_id"]= user[0]
    session["user_name"] = name
    session["user_role"] = user[2]
    result = db.session.execute(text("SELECT id, name FROM quizzes WHERE visible=1"))
    quizzes = result.fetchall()
    return render_template("quiz.html", quizzes=quizzes)

@app.route("/userstat")
def userstat():
    return render_template("userstat.html")

@app.route("/new_quiz")
def new_quiz():
    return render_template("create_quiz.html")

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
    return redirect("/answers")

@app.route("/answers")
def answers():
    result = db.session.execute(text("SELECT id, question FROM questions WHERE quiz_id=7")) 
    questions = result.fetchall()
    return render_template("answers.html", questions=questions)
