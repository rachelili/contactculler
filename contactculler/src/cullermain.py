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
                            'FROM Contact '
                            'WHERE ANCESTOR IS :1 '
                            'ORDER BY name ASC LIMIT 10',
                            guestbook_key)
        context["data"]=""
        context["contacttypeoptions"] = '<option value="HumanContact" selected>Person</option>\n<option value="BusinessContact">Business</option>'
        for contact in contacts:
            if contact.owner: #if an owner exists
                context["data"]+='<b>%s</b> wrote: ' % contact.owner.nickname() #show their nickname
                context["data"]+= '<p> name =' + contact.name + '</p>' #and their company name
            else:
                context["data"]+='An anonymous person wrote:'
            #context["data"]+='<blockquote>%s</blockquote>' % cgi.escape(contact.content) 
            #to print < or > or &, use "&(amp, gt, lt);" for which you need cgi.escape
            
            # get all contact fields whose ancestor is contact.key
            # loop through contact fields and put them into context["data"]
            
            
        context["contactfields_dict"] = {"phone_home": "Phone (home)",
                                "phone_mobile": "Phone (mobile)",
                                "address_home": "Address (home)"}
        return self.response.out.write(template.render(context))


class Guestbook(webapp2.RequestHandler):
    def post(self):
        logging.info("cullermain.Guestbook.post(): Got here!")
        if users.get_current_user(): #if there is a user
            contacttype = self.request.get('ContactType')
            if contacttype == 'BusinessContact':
                greeting = DataStructures.BusinessContact(parent=guestbook_key)
                greeting.name = self.request.get('name') #display single name entry
            elif contacttype == 'HumanContact':
                greeting = DataStructures.HumanContact(parent=guestbook_key)
                greeting.firstname = self.request.get('firstname') #display first name entry
                greeting.lastname = self.request.get('lastname') #display last name entry    
            else:
                logging.error('cullermain.Guestbook.post(): Unknown contact type ='+str(contacttype))
            greeting.owner = users.get_current_user() #set the owner to the user
            greeting.put() #put it into the template
            greeting_key = greeting.key  # the parent of the contact fields
            # this should be from DB   "select (star) from ContactFieldTypes" 
            contactfields_dict = {"phone_home": "Phone (home)",
                                "phone_mobile": "Phone (mobile)",
                                "address_home": "Address (home)"}
            
            for key in contactfields_dict:
                if self.request.get_all(key):
                    logging.info("self.request.get(key) = "+str(self.request.get_all(key)))  
                    for contactfield_value in self.request.get_all(key):
                        logging.info( "key = "+str( key)+ " value = " + str(contactfield_value))
                        # save contact field in DB with parent = greeting_key
                        # key = contact field type
                        #value = contractfield_value
        
        self.redirect('/home') #return to the homepage
    
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