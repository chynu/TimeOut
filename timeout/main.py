import webapp2
import os
import jinja2
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader =
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

# ================== HANDLERS ===================
# actual handlers
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
class FeelingHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

# test handlers
class CelineTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())
class NigelTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/response.html')
        self.response.write(template.render())
class PeteTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/write.html')
        self.response.write(template.render())

# ================ OBJECTS =================
# user object, for each login. ONLY instantiated when a person logs in with gmail username.
class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    compliment_list = ndb.KeyProperty('Compliment', repeated=True)

# compliment object, created every time someone WRITES a compliment.
# called every time someone ASKS FOR a compliment.
class Compliment(ndb.Model):
    content = ndb.StringProperty(required=True)
    points = ndb.IntegerProperty(required=True)
    views = ndb.IntegerProperty(required=True)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/celix', CelineTestHandler),
    ('/nigel', NigelTestHandler),
    ('/pete', PeteTestHandler)
], debug=True)
