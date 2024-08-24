from db import db
from sqlalchemy.sql import text

def get_point(user_id, quiz_id, quest_id):
    sql = text("SELECT * FROM apoints WHERE user_id=:user_id AND quiz_id=:quiz_id AND quest_id=:quest_id")
    return db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id, "quest_id":quest_id}).fetchone()

def give_point(user_id,quiz_id, quest_id):
        sql = text("INSERT INTO apoints (user_id, quiz_id, quest_id, points) VALUES (:user_id, :quiz_id, :quest_id, :points)")
        db.session.execute(sql,{"user_id":user_id, "quiz_id":quiz_id, "quest_id":quest_id,"points":1})
        db.session.commit() 

def count_attendance(user_id):
    sql = text("SELECT COUNT( DISTINCT(quiz_id)) FROM apoints WHERE user_id=:user_id")
    return db.session.execute(sql, {"user_id":user_id}).fetchone()[0]

def count_points(user_id):
    sql = text("SELECT COUNT(points) FROM apoints WHERE user_id=:user_id")
    return db.session.execute(sql, {"user_id":user_id}).fetchone()[0]