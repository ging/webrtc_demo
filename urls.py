#-*- coding: utf-8 -*-
'''Urls for blog app'''
from webapp2 import Route
from webapp2_extras import routes

urls = [
    routes.HandlerPrefixRoute('webrtc.handlers.', [
        Route(r'/', handler='IndexHandler', name='home'),
        Route(r'/sign_in', handler='SignInHandler', name='signin'),
        Route(r'/wait', handler='WaitHandler', name='wait'),
        Route(r'/message', handler='MessageHandler', name='message'),
        Route(r'/sign_out', handler='SignOutHandler', name='signout'),
        Route(r'/timeout', handler='TimeoutHandler', name='signout'),
    ]),
]
