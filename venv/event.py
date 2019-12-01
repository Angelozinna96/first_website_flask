#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:54:50 2019

@author: angelozinna
"""

from app import app, db
from app.models import User, Event,Sharedevent

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event,'Sharedevent':Sharedevent}