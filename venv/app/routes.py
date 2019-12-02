#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:28:33 2019

@author: angelozinna
"""
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user,logout_user, login_required
from app.models import User, Event, Sharedevent
from app import app
from app.forms import LoginForm, RegistrationForm, CreateEventForm, SearchForm, DeleteEventForm, ModifyEventForm, ArchiveEventForm, SharedEventForm
from flask import request
from werkzeug.urls import url_parse
from app import db


@app.route('/')
@app.route('/index')
@login_required
def index():

    events = Event.query.filter(Event.user_id==current_user.get_id()).filter(Event.archived=="no").all()
    return render_template('index.html', title='Home', events=events)

@app.route('/event_shared')
@login_required
def eventshared():   
    user_id = Sharedevent.query.join(User,Sharedevent.user_id1==User.id).join(Event,Sharedevent.event_shared==Event.id).filter(Event.archived=="no").all()
    
    #retrieve the event information from the event id
    events = db.session.query(Sharedevent,Event,User).filter(Sharedevent.user_id2==current_user.get_id()).filter(Sharedevent.user_id1==User.id).filter(Sharedevent.event_shared==Event.id).filter(Event.archived=="no").all()
    
    return render_template('eventshared.html', title='Event Shared with you', events=events)

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

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if form.search.data.strip() == "":
            events = Event.query.filter(Event.archived=="no").all()   
            flash("The event has not been found!")
        else:
             events = Event.query.filter(Event.name.like(form.search.data+"%")).filter(Event.archived=="no").all()
             flash("Events has been found!")
    else:
        flash("The event has not been found!")
        events = Event.query.filter(Event.archived=="no").all()
    return render_template('search.html', title='Search', form=form, events=events)

@app.route('/share_event', methods=['GET', 'POST'])
@login_required
def shareevent():
    form = SharedEventForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        ev_id = Event.query.filter(Event.id==form.id_event.data).first()
        #query if already exist the entry
        if user is not None:
            shared=Sharedevent.query.filter(Sharedevent.user_id1==current_user.get_id()).filter(Sharedevent.user_id2==user.id).filter(Sharedevent.event_shared==form.id_event.data).first()
        if user is None :         
            flash("User not exist!")
        elif ev_id is None:           
            flash("Event not exist!")
        elif shared is not None:           
            flash("You have already shared this event to this user!")
        else:
            event=Sharedevent(user_id1=current_user.get_id(), user_id2=user.id, event_shared=form.id_event.data)
            db.session.add(event)
            db.session.commit()
            flash('Congratulations, your event is been shared!')
 
    events = Event.query.filter(Event.archived=="no").all()
    return render_template('shareevent.html', title='Share Event', form=form, events=events)


@app.route('/delete_event', methods=['GET', 'POST'])
@login_required
def deleteevent():
    form = DeleteEventForm()
    if form.validate_on_submit():
        event_to_delete = Event.query.filter(Event.id==form.id_event.data).first()
        #control if it is allowed to delete the post
        if str(event_to_delete.user_id) == str(current_user.get_id()):
            db.session.delete(event_to_delete)
            db.session.commit()
            flash('You have successfully removed the event!') 
        else:
            flash('You can not delete events of other users!')   
    events = Event.query.filter(Event.user_id==current_user.get_id()).all()
    return render_template('deleteevent.html', title='Delete Event', events=events, form=form)

@app.route('/modify_event', methods=['GET', 'POST'])
@login_required
def modifyevent():
    form = ModifyEventForm()
    if form.validate_on_submit():
        event_to_modify = Event.query.filter(Event.id==form.id_event.data).first()
        #control if it is allowed to delete the post
        if str(event_to_modify.user_id) == str(current_user.get_id()):           
            db.session.delete(event_to_modify)
            db.session.commit()
            event=Event(name=form.name.data, addr_1=form.addr_1.data,location=form.location.data, datetime_start=form.datetime_start.data, user_id=current_user.get_id())
            db.session.add(event)
            db.session.commit()
            flash('You have successfully modified the event!')  
        else:
            flash('You can not modify events of other users!')   
    return render_template('modifyevent.html', title='Modify Event', form=form)

@app.route('/archive_event', methods=['GET', 'POST'])
@login_required
def archiveevent():
    form = ArchiveEventForm()
    if form.validate_on_submit():
        event_to_archive = Event.query.filter(Event.id==form.id_event.data).first()
        #control if it is allowed to delete the post
        if str(event_to_archive.user_id) == str(current_user.get_id()):           
            db.session.delete(event_to_archive)
            db.session.commit()
            event=Event(archived="yes", name=event_to_archive.name, addr_1=event_to_archive.addr_1,location=event_to_archive.location, datetime_start=event_to_archive.datetime_start, user_id=current_user.get_id())
            db.session.add(event)
            db.session.commit()
            flash('You have successfully archived the event!')  
        else:
            flash('You can not archive events of other users!')   
    events = Event.query.filter(Event.user_id==current_user.get_id()).filter(Event.archived=="no").all()
    return render_template('archiveevent.html', title='Archive Event', events=events, form=form)

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
        event=Event(name=form.name.data, addr_1=form.addr_1.data, location=form.location.data,datetime_start=form.datetime_start.data, user_id=current_user.get_id())
        db.session.add(event)
        db.session.commit()
        flash('Congratulations, your event is been created!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('createevent.html', title='Create Event', form=form)
