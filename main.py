import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>
              Welcome to DC Food Truck Battle site
            </body>
          </html>""")


class Sms(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('From')))
        self.response.out.write('<br/>')
        self.response.out.write(cgi.escape(self.request.get('Body')))
        self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sms', Sms)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()