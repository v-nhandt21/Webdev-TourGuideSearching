#from app import db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Guide(db.Model):
    __tablename__ = 'guides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.Integer())
    gender = db.Column(db.Integer())
    age= db.Column(db.Integer())

    def __init__(self, name, password, gender,age):
        self.name = name
        self.password = abs(hash(password)) % (10 ** 8)
        self.gender = gender
        self.age = age

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'password': self.password,
            'gender':self.gender,
            'age':self.age
        }