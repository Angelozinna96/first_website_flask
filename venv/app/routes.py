#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:28:33 2019

@author: angelozinna
"""
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user,logout_user, login_required
from app.models import User
from app import app
from app.forms import LoginForm, RegistrationForm, CreateEventForm
from flask import request
from werkzeug.urls import url_parse
from app import db

@app.route('/')
@app.route('/index')
@login_required
def index():

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_passwd(form.password.data):
            flash('Login failed : invalid username or password! ')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,firstname=form.firstname.data,lastname=form.lastname.data)
        user.set_passwd(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def createevent():
    form = CreateEventForm()
    if form.validate_on_submit():
        flash('event {} Successfull created!'.format(
            form.name.data))
        return redirect(url_for('index'))
    return render_template('createevent.html', title='Create Event', form=form)