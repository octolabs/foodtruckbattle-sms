import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import utils
import settings

class MainPage(webapp.RequestHandler):
    def get(self):
		all = db.GqlQuery("SELECT * FROM Truck ORDER BY counter DESC")

		msg=""
		count=0
		for truck in all:
			count=count+1
			if count<4:
				msg=msg+"<b>"+truck.name+" ("+truck.short+") - "+str(truck.counter)+" votes </b><br/> "
			else:
				msg=msg+truck.name+" ("+truck.short+") - "+str(truck.counter)+" votes <br/> "

		self.response.out.write("""
		<html>
		<body>
		<center>
		<img src="/static/logo.jpg"/>
		<br/>
		Welcome to DC Food Truck Battle site
		<br/>
		<br/>
		<b>LEADERBOARD</b>
		<br/>
		<br/>
		%s
		
		<br/>
		<br/>
		<i>To vote, send SMS with your favorite truck handle to (202) 559-4219.</i>
		</center>
		</body>
		</html>""" % (msg))


class Sms(webapp.RequestHandler):
    def get(self):
		phone=cgi.escape(self.request.get('From'))
		msg=cgi.escape(self.request.get('Body'))

		if msg in settings.foodtrucks:
			utils.incrementCounter(msg)		
			
			response=utils.getTop3()

			self.response.headers["Content-Type"] = "text/xml"
			self.response.out.write("""<?xml version="1.0" encoding="UTF-8"?>
			<Response>
			    <Sms>%s</Sms>
			</Response>
			""" % (response))
			
		else:
			#unrecognized truck name
			response = "Sorry, we can't recognize food truck with handle - %s, Please, check food truck handle and vote again!" % (msg)
			
			self.response.headers["Content-Type"] = "text/xml"
			self.response.out.write("""<?xml version="1.0" encoding="UTF-8"?>
			<Response>
			    <Sms>%s</Sms>
			</Response>
			""" % (response))

		#log this vote
		vote=models.Vote()
		vote.phone=phone
		vote.msg=msg
		#vote.put()	



application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sms', Sms)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()