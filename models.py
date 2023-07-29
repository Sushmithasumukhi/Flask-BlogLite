import os
import requests
from flask import Flask , request , render_template, url_for, redirect, session, flash, make_response
from flask_restful import Resource,Api,fields,marshal_with,reqparse 
from werkzeug.exceptions import HTTPException
import json
from werkzeug.utils import secure_filename 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime as d 

current_dir=os.path.abspath(os.path.dirname(__file__))

BASE="http://127.0.0.1:8080"

app=Flask(__name__)
app.secret_key = 'project'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"database.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy()
db.init_app(app)

api=Api(app)
app.app_context().push()


# -----------------------------------------------------------Models------------------------------------------------------------------

class Follows(db.Model):
    __tablename__ = 'follows'
    followerid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followingid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String , unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    dob = db.Column(db.String)
    profession = db.Column(db.String)
    about_user = db.Column(db.String)
    image = db.Column(db.String, nullable = False, default='default.jpg')
    posts = db.relationship('Post' , backref='user', cascade = 'all,delete')
    followers = db.relationship('Follows', foreign_keys=[Follows.followingid],backref=db.backref('following', lazy='joined'),lazy='dynamic',cascade = 'all,delete')
    following = db.relationship('Follows', foreign_keys=[Follows.followerid],backref=db.backref('follower', lazy='joined'),lazy='dynamic',cascade = 'all,delete')
    cmts = db.relationship('Comment' , backref='user', cascade = 'all,delete')
    l = db.relationship('Like' , backref='user', cascade = 'all,delete')

class Post(db.Model):
    __tablename__='posts'
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    photo1 = db.Column(db.String)
    photo2 = db.Column(db.String)
    photo3 = db.Column(db.String)
    photo4 = db.Column(db.String)
    datetime=db.Column(db.DateTime(timezone=True), server_default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE") , nullable=False)
    cmts = db.relationship('Comment' , backref='posts', cascade = 'all,delete')
    l = db.relationship('Like' , backref='posts', cascade = 'all,delete')

class Comment(db.Model):
    __tablename__='comments'
    cmt_id = db.Column(db.Integer, primary_key=True)
    cmt_body = db.Column(db.String)
    cmt_creater = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE") , nullable=False)
    post_cmted =  db.Column(db.Integer, db.ForeignKey("posts.post_id", ondelete="CASCADE") , nullable=False)

class Like(db.Model):
    __tablename__='likes'
    like_id = db.Column(db.Integer, primary_key=True)
    liked_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE") , nullable=False)
    post_liked = db.Column(db.Integer, db.ForeignKey("posts.post_id", ondelete="CASCADE") , nullable=False)

