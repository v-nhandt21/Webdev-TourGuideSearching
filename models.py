#from app import db
from flask_sqlalchemy import SQLAlchemy
import hashlib
db = SQLAlchemy()
class Guide(db.Model):
    __tablename__ = 'guides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    gender = db.Column(db.String())
    age= db.Column(db.String())
    rating = db.Column(db.String())
    list_review=db.Column(db.String())    #String split each review by ;
    avatar = db.Column(db.String())
    bio =db.Column(db.String())
    language =db.Column(db.String())
    cred = db.Column(db.String())
    location = db.Column(db.String())
    videolink= db.Column(db.String())
    cvlink =db.Column(db.String())
    linkin = db.Column(db.String())
    email =db.Column(db.String())
    act_level = db.Column(db.String())
    exp = db.Column(db.String())
    price_hour = db.Column(db.String())
    address = db.Column(db.String())
    freetime = db.Column(db.String()) #1a -> 7c
    phone = db.Column(db.String())
    calender = db.Column(db.String())



    def __init__(self, name, password, gender,age,rating,list_review,avatar,bio,language,cred,location,videolink,cvlink,linkin,email,act_level,exp,price_hour,address,freetime,phone,calender):
        self.name = name
        self.password = str(int(hashlib.sha1(password.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
        self.gender = gender
        self.age = age
        self.rating = rating
        self.list_review=list_review
        self.avatar = avatar
        self.bio =bio
        self.language =language
        self.cred = cred
        self.location = location
        self.videolink= videolink
        self.cvlink =cvlink
        self.linkin = linkin
        self.email =email
        self.act_level = act_level
        self.exp = exp
        self.price_hour = price_hour
        self.address = address
        self.freetime = freetime
        self.phone = phone
        self.calender = calender


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'password': self.password,
            'gender':self.gender,
            'age':self.age,
            'rating':self.rating,
            'list_review':self.list_review,
            'avatar':self.avatar,
            'bio':self.bio,
            'language':self.language,
            'cred':self.cred,
            'location':self.location,
            'videolink':self.location,
            'cvlink':self.cvlink,
            'linkin':self.linkin,
            'email':self.email,
            'act_level':self.act_level,
            'exp':self.exp,
            'price_hour':self.price_hour,
            'address':self.address,
            'freetime':self.freetime,
            'phone':self.phone,
            'calender':self.calender,
        }