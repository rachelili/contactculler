'''
Created on Apr 14, 2014

@author: Rachel
'''
from google.appengine.ext import ndb

class Contact(ndb.Model):
    owner = ndb.UserProperty()

class HumanContact(Contact): #HumanContact, which is also a Contact
    lastname = ndb.StringProperty() #the last name of the humann, which is a string
    firstname = ndb.StringProperty() #the firstname of the human, which is a string
    
class BusinessContact(Contact): #BusinessContact, which is also a Contact
    name = ndb.StringProperty() #the name of the company, which is a string
    
class ContactFieldType(ndb.Model): #ContactFieldType, which contains a name for the Field Type
    name = ndb.StringProperty() #the name is in the form of a string

class ContactField(ndb.Model): #ContactField, which contains a type (label) and a value (containing an email, number, etc)
    type = ndb.KeyProperty() #the type is a key in the dictionary ContactField??
    value = ndb.StringProperty() #the value - which the user inputs - is in the form of a string
    
class Greeting(ndb.Model):      #goal: turn Greeting into BusinessContact
    owner = ndb.UserProperty()  #the owner is the user
    content = ndb.TextProperty() #the content is text
    name = ndb.StringProperty() #the name is a string
    date = ndb.DateTimeProperty(auto_now_add=True) #date is current date/time
    
    
    

