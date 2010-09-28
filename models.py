from google.appengine.ext import db

class Vote(db.Model):
	phone =  db.StringProperty()
	msg = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)

class Truck(db.Model):
	name = db.StringProperty()
	short = db.StringProperty()
	count = db.IntegerProperty()