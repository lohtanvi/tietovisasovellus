from db import db
from sqlalchemy.sql import text

def get_creator_quizzes(creator_id):
    sql = text("SELECT id, name FROM quizzes WHERE visible=1 AND creator_id=:creator_id")
    return db.session.execute(sql, {"creator_id":creator_id}).fetchall()

def get_creator_noquizzes(creator_id):
    sql = text("SELECT id, name FROM quizzes WHERE visible=0 AND creator_id=:creator_id")
    return db.session.execute(sql, {"creator_id":creator_id}).fetchall() 

def get_visible_quizzes():
    sql = text("SELECT id, name FROM quizzes WHERE visible=1")
    return db.session.execute(sql).fetchall()

def get_novisible_quizzes():
    sql = text("SELECT id, name FROM quizzes WHERE visible=0")
    return db.session.execute(sql).fetchall()

def set_quiz_invisible(id):
    sql = text("UPDATE quizzes SET visible = 0 WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit() 

def set_quiz_visible(id):
    sql = text("UPDATE quizzes SET visible = 1 WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def create_quiz_name(creator_id,name):
    sql = text("INSERT INTO quizzes (creator_id, name, visible) VALUES (:creator_id, :name, :visible) RETURNING id")
    return db.session.execute(sql, {"creator_id":creator_id,"name":name,"visible":1}).fetchone()[0]

def count_quizzes(creator_id):
    sql = text("SELECT COUNT(name) FROM quizzes WHERE creator_id=:creator_id")
    return db.session.execute(sql, {"creator_id":creator_id}).fetchone()[0]

def count_noquizzes(creator_id):
    sql = text("SELECT COUNT(name) FROM quizzes WHERE creator_id=:creator_id AND visible=:visible")
    return db.session.execute(sql, {"creator_id":creator_id,"visible":0}).fetchone()[0]