#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:52:45 2019

@author: angelozinna
"""

import os 
class Config(object):
     SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-know" 