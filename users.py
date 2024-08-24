from db import db
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash


def get_users_data(name):
    sql = text("SELECT id, password, role FROM users WHERE name=:name")
    return db.session.execute(sql, {"name":name}).fetchone()

def create_user(name,password,role):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (name, password, role) VALUES (:name, :password, :role)")
    db.session.execute(sql, {"name":name,"password":hash_value,"role":role})
    db.session.commit()
    return True

