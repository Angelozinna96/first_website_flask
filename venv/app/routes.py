#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:28:33 2019

@author: angelozinna
"""
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, SignupForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('user {} Successfull Registered! Now log in!'.format(
            form.username.data))
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)