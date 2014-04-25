'''
Created on Apr 25, 2014

@author: Rachel
'''
    #!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import datetime
import webapp2
import logging
import jinja2
import os
import DataStructures
#import google.appengine.ext
from google.appengine.ext import ndb
from google.appengine.api import users

guestbook_key = ndb.Key('key', 'value')


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))

class MainPage(webapp2.RequestHandler):
    def get(self):
    #self.response.out.write('<html><body>')
        user = users.get_current_user()
        context={}

        if user:
            context["nickname"]=user.nickname()
            context["signout_url"] = users.create_logout_url("/")
            context["is_admin"] = users.is_current_user_admin()
#             self.response.out.write(
#                 'Hello %s <a href="%s">Sign out</a><br>Is administrator: %s' % 
#                 (user.nickname(), users.create_logout_url("/"), users.is_current_user_admin())
#             )
        else:
            self.redirect("/")
            
        template = jinja_environment.get_template("index.html")
        
        contacts = ndb.gql('SELECT * ' #pulls from database
                            'FROM Greeting '
                            'WHERE ANCESTOR IS :1 '
                            'ORDER BY date DESC LIMIT 10',
                            guestbook_key)
        context["data"]=""
        for contact in contacts:
            if contact.owner: #if an owner exists
                context["data"]+='<b>%s</b> wrote: ' % contact.owner.nickname()
                context["data"]+= 'name = ' + contact.name
            else:
                context["data"]+='An anonymous person wrote:'
            context["data"]+='<blockquote>%s</blockquote>' % cgi.escape(contact.content)
        return self.response.out.write(template.render(context))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        greeting = DataStructures.Greeting(parent=guestbook_key)
        
        if users.get_current_user():
            greeting.owner = users.get_current_user()
        greeting.name = self.request.get('name')
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/home')
    
class SignIn(webapp2.RequestHandler):
    
    
    def get(self):
        context = {}
        template = jinja_environment.get_template("signin.html")
        user = users.get_current_user()

        if user:
            self.redirect("/home")
            
        else:
            context["signin_url"]=users.create_login_url("/home")
            
        return self.response.out.write(template.render(context))

            

app = webapp2.WSGIApplication([
  ('/', SignIn),
  ('/sign', Guestbook),
  ('/home', MainPage)
], debug=True)