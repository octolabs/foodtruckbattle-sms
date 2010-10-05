import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import utils
import settings

class AdminPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>
				<center>
				<img src="/static/logo.jpg"/>
				<br/>
              Welcome to DC Food Truck Battle admin page
				<br/>
				<br/>
				<a href="/admin/reset">Reset app</a>
				<br/>
				<br/>
				<a href="/admin/init">Initialize app</a>
				</center>
            </body>
          </html>""")


class Init(webapp.RequestHandler):
    def get(self):
		#populate counters database with zeros
		for truck in settings.foodtrucks:
			tr=models.Truck(key_name=truck) #key=truck
			tr.name=settings.foodtrucks[truck]
			tr.short=truck
			tr.counter=0
			tr.put()
			
		self.redirect("/admin/")


class Reset(webapp.RequestHandler):
    def get(self):
		#erase all values from database
		votes=models.Vote.all()
		db.delete(votes)

		trucks=models.Truck.all()
		db.delete(trucks)
		
		self.redirect("/admin/init")
		


application = webapp.WSGIApplication(
                                     [('/admin/', AdminPage),
                                      ('/admin/reset', Reset),
									  ('/admin/init', Init)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()