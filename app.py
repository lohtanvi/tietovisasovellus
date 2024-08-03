from flask import Flask
from flask import redirect, render_template, session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

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
    result = db.session.execute(text("SELECT id, name FROM quizzes"))
    quizzes = result.fetchall()
    return render_template("quiz.html", name=request.form["name"], quizzes=quizzes)



#@app.route("/new_quiz", methods=["POST"])
#    def new_quiz():
#    name = requst.form("new_quiz")
#    creator_id = 2
#    visible = 1
     
