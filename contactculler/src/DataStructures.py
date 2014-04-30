'''
Created on Apr 14, 2014

@author: Rachel
'''
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Contact(polymodel.PolyModel):
    owner = ndb.UserProperty()
    name = ndb.ComputedProperty(lambda self: None)

class HumanContact(Contact): #HumanContact, which is also a Contact
    lastname = ndb.StringProperty() #the last name of the humann, which is a string
    firstname = ndb.StringProperty() #the firstname of the human, which is a string
    #fullname is defined in cullermain, concatenating first+last for display purposes
    name = ndb.ComputedProperty(lambda self: self.firstname+' '+self.lastname) #computed = take its own properties
    
class BusinessContact(Contact): #BusinessContact, which is also a Contact
    name = ndb.StringProperty() #the name of the company, which is a string
    
class ContactFieldType(polymodel.PolyModel): #ContactFieldType, which contains a name for the Field Type
    name = ndb.StringProperty() #the name is in the form of a string

class ContactField(polymodel.PolyModel): #ContactField, which contains a type (label) and a value (containing an email, number, etc)
    type = ndb.KeyProperty() #the type is a key in the dictionary ContactField??
    value = ndb.StringProperty() #the value - which the user inputs - is in the form of a string
    note = ndb.TextProperty() #for notes about each field
    date = ndb.DateTimeProperty(auto_now = True)
    
#class Greeting(ndb.Model):      #goal: turn Greeting into BusinessContact
    #owner = ndb.UserProperty()  #the owner is the user
    #content = ndb.TextProperty() #the content is text
    #name = ndb.StringProperty() #the name is a string
    #date = ndb.DateTimeProperty(auto_now_add=True) #date is current date/time
    
    
    

