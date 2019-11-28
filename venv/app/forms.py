#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 09:21:53 2019

@author: angelozinna
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()]) 
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Sign In")
    
class SignupForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()]) 
    lastname = StringField("Lastname", validators=[DataRequired()]) 
    username = StringField("Username", validators=[DataRequired()]) 
    password = PasswordField("Password", validators=[DataRequired()])
    dateofbirth = DateField("Date of birth(dd/mm/yyyy)",validators=[DataRequired()],format='%d-%m-%Y')
    submit = SubmitField("Sign Up")
    
    