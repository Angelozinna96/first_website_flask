#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:52:45 2019

@author: angelozinna
"""

import os 
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
     SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-know" 
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
     SQLALCHEMY_TRACK_MODIFICATIONS = False