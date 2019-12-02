#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:38:30 2019

@author: angelozinna
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=True)
    lastname = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def set_passwd(self,passwd):
        self.password_hash= generate_password_hash(passwd)
    def check_passwd(self,passwd):
        return check_password_hash(self.password_hash,passwd)

    def __repr__(self):
        return '<id = {} name = {}>'.format(self.id,self.username)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64),index=True)
    addr_1 =  db.Column(db.String(120),index=True)
    location = db.Column(db.String(120),index=True)
    datetime_start =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    datetime_end = db.Column(db.DateTime, default=datetime.utcnow)
    archived = db.Column(db.String(10),default="no",index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Event name={}, addr_1={},location={}, datetime_start={},archived={}, user_id={}>'.format(self.name,self.addr_1,self.location,self.datetime_start,self.archived,self.user_id)
    
class Sharedevent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_shared = db.Column(db.Integer, db.ForeignKey('event.id'))
    

    def __repr__(self):
        return '<SharedEvent user={}-->user={} event={}>'.format(self.user_id1,self.user_id2,self.event_shared)