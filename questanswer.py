from db import db
from sqlalchemy.sql import text

def create_question(quiz_id,question):
    sql = text("INSERT INTO questions (quiz_id, question, qvisible) VALUES (:quiz_id, :question, :qvisible)")
    db.session.execute(sql, {"quiz_id":quiz_id,"question":question,"qvisible":1})
    db.session.commit()

def get_answers(quest_id):
    sql = text("SELECT * FROM qanswers WHERE quest_id=:quest_id")
    return db.session.execute(sql, {"quest_id":quest_id}).fetchone()

def get_questions(quiz_id):
    sql = text("SELECT id, question FROM questions WHERE quiz_id=:quiz_id AND qvisible=:qvisible")
    return db.session.execute(sql, {"quiz_id":quiz_id,"qvisible":1}).fetchall()

def get_quiz_id(id):
    sql = text("SELECT quiz_id FROM questions WHERE id=:id")
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def create_answer(answer,quest_id):
    sql = text("INSERT INTO qanswers (answer, quest_id, correct) VALUES (:answer, :quest_id, :correct)")
    db.session.execute(sql, {"answer":answer,"quest_id":quest_id,"correct":1})
    db.session.commit()

def create_answerchoice(answer,quest_id):
    sql = text("INSERT INTO qanswers (answer, quest_id, correct) VALUES (:answer, :quest_id, :correct)")
    db.session.execute(sql, {"answer":answer,"quest_id":quest_id,"correct":0})
    db.session.commit() 

def get_answerchoice(quest_id):
    sql = text("SELECT * FROM qanswers WHERE quest_id=:quest_id ORDER BY answer ASC")
    return db.session.execute(sql, {"quest_id":quest_id}).fetchall()

def get_correct_answer(quest_id):
    sql = text("SELECT answer FROM qanswers WHERE quest_id=:quest_id AND correct=1")
    return db.session.execute(sql, {"quest_id":quest_id}).fetchone()[0]

def set_question_invisible(id):
    sql = text("UPDATE questions SET qvisible = 0 WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit() 

def add_question(quiz_id,question):
    sql = text("INSERT INTO questions (quiz_id, question, qvisible) VALUES (:quiz_id, :question, :qvisible) RETURNING id")
    id = db.session.execute(sql, {"quiz_id":quiz_id,"question":question,"qvisible":1}).fetchone()[0]
    db.session.commit()
    return id