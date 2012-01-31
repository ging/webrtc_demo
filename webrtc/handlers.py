#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
import webapp2
import random
import datetime

from google.appengine.ext.webapp import template


from google.appengine.ext import db

from .models import User, Message

class BaseHandler(webapp2.RequestHandler):
    """
        Handler base to implement templates and other stuff.
    """
   
    def render_template(self, filename, **template_args):
        path = 'templates/' + filename
        self.response.write(template.render(path, template_args))
    
    def get_user(self, peer_id):
        query = User.all().filter('peer_id = ',int(peer_id))
        instance = query.get()
        return instance
        
    def create_user(self, name):
        peer_id = random.randint(0,10000)
        user = self.get_user(peer_id)
        if user:
            return self.create_user(name)

        args = {
            'name': name,
            'peer_id': peer_id,
        }
        new_user = User(**args)
        new_user.put()
        return new_user
        
    def delete_user(self, peer_id):
        old_user = self.get_user(peer_id)
        old_user.delete()
        users = User.all()
        for user in users:
            self.create_message(user.peer_id, user.peer_id, old_user.name + ',' + str(old_user.peer_id) + ',0')

        
    def create_message(self, from_id, to_id, msg):
        args = {
            'msg': msg,
            'from_id': from_id,
            'to_id': to_id,
        }
        new_msg = Message(**args)
        new_msg.put()
        
class IndexHandler(BaseHandler):
    """
        Home page handler
    """
    def get(self):
        return self.render_template('index.html')

class SignInHandler(BaseHandler):
    """
        Sign-in handler
    """
    def get(self):
    
        """
            HTTP GET verb.
        """
        users = User.all()
        user_str = ''
        for user in users:
            user_str = user_str + user.name + ',' + str(user.peer_id) + '\n'

        new_user = self.create_user(self.request.query_string)
        
        user_str = new_user.name + ',' + str(new_user.peer_id) + '\n' + user_str
		
        for user in users:
            if user.peer_id != new_user.peer_id:
                self.create_message(user.peer_id, user.peer_id, new_user.name + ',' + str(new_user.peer_id) + ',1')
        return self.response.write(user_str)
        
class SignOutHandler(BaseHandler):
    """
        Sign-out handler
    """
    def get(self):

        peer_id = self.request.get('peer_id')
        if peer_id:
            print
            self.delete_user(peer_id)

class WaitHandler(BaseHandler):
    """
        Wait handler
    """
    
    def get(self):
    
        peer_id = self.request.get('peer_id')
        pragma_id = peer_id
        query = Message.all().filter('to_id = ',int(peer_id)).order("created")
        next_message = query.get()
        if next_message:
            pragma_id = next_message.from_id
            self.response.write(next_message.msg)
            next_message.delete()
        else:
            self.response.set_status(304, "No need to do anything")
        self.get_user(peer_id).put()
        self.response.headers.add_header("Pragma", str(pragma_id))
        
class MessageHandler(BaseHandler):
    """
        Message handler
    """
    
    def post(self):
        peer_id = int(self.request.get('peer_id'))
        to_id = int(self.request.get('to'))
        msg = self.request.body
        self.create_message(peer_id, to_id, msg)
        
class TimeoutHandler(BaseHandler):
    """
        Timeout handler. To be called by cron tasks
    """
    
    def get(self):
        for old_user in User.all():
            if old_user:
                if (datetime.datetime.now() - (old_user.updated)).seconds > 30:
                    self.delete_user(old_user.peer_id)
