#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:38:30 2019

@author: angelozinna
"""

from app import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=True)
    lastname = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64),index=True)
    addr_1 =  db.Column(db.String(120),index=True)
    location = db.Column(db.String(120),index=True)
    datetime_start =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    datetime_end = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Event {}>'.format(self.body)