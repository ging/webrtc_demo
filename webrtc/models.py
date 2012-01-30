#!/usr/bin/env python
#-*- coding:utf-8 -*-

from google.appengine.ext import db

import webapp2_extras.json

class User(db.Model):
    name = db.TextProperty()
    peer_id = db.IntegerProperty(default=0)
    updated = db.DateTimeProperty(auto_now=True)
    
class Message(db.Model):
    from_id = db.IntegerProperty(default=0)
    to_id = db.IntegerProperty(default=0)
    msg = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)