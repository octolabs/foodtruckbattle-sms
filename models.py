from google.appengine.ext import db

#model to store every single vote (if possible)
class Vote(db.Model):
	phone =  db.StringProperty()
	msg = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)

#model to store total vote counts per truck
class Truck(db.Model):
	name = db.StringProperty()
	short = db.StringProperty()
	counter = db.IntegerProperty()