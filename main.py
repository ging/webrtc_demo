#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
import webapp2

# add lib to pythonpath
# Is important to do this before try to import webapp2_extras and others from
# lib
#current_path = os.path.abspath(os.path.dirname(__file__))
#sys.path[0:0] = [
#    os.path.join(current_path, 'lib'),
#]

import urls

# find dev server in environ to determine debug status
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
# if nose module is loaded, testing is in progress
if 'nose' in sys.modules: debug = True

app = webapp2.WSGIApplication(routes=urls.urls, debug=debug)

def main():
    app.run()

if __name__ == '__main__':
    main()
