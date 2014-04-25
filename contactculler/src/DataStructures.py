'''
Created on Apr 14, 2014

@author: Rachel
'''
from google.appengine.ext import ndb

class Contact(ndb.Model):
    owner = ndb.UserProperty()

class HumanContact(Contact):
    lastname = ndb.StringProperty()
    firstname = ndb.StringProperty()
    
class BusinessContact(Contact):
    name = ndb.StringProperty()
    
class ContactFieldType(ndb.Model):
    name = ndb.StringProperty()

class ContactField(ndb.Model):
    type = ndb.KeyProperty()
    value = ndb.StringProperty()
    
class Greeting(ndb.Model):
    owner = ndb.UserProperty()
    content = ndb.TextProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    
    

