#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 09:21:53 2019

@author: angelozinna
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()]) 
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Sign In")
class SearchForm(FlaskForm):
    search = StringField("Search for event name",default="") 
    submit = SubmitField("Search")
class CreateEventForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()]) 
    addr_1 = StringField("Address line 1", validators=[DataRequired()]) 
    location = TextAreaField("Description", validators=[DataRequired()]) 
    datetime_start =  DateTimeField("Datetime start((yyyy-mm-dd HH:mm))", validators=[DataRequired()], format ='%Y-%m-%d %H:%M')
    user_id = IntegerField("User_id",validators=[DataRequired()])
    submit = SubmitField("Create")
    def validate_user_id(self, user_id):
        us = User.query.filter_by(id=user_id.data).first()
        if us is None:
            raise ValidationError('Please use a real User_id')
class RegistrationForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()]) 
    lastname = StringField("Lastname", validators=[DataRequired()]) 
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    