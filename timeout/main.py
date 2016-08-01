import webapp2
import os
import jinja2
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader =
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

# ================== HANDLERS ====================
# actual handlers
class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

class ResponseHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/response.html')
        added_points = int(self.request.get('points'))
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/response_confirm.html')
        self.response.write(template.render())

class WriteHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/write.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/write_confirm.html')
        new_compliment = self.request.get('words')
        complimentObj = Compliment(content=new_compliment,points= 0,views= 0)
        comp_key = complimentObj.put()



# test handlers
class IndexTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())
class ResponseTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/response.html')
        self.response.write(template.render())
class WriteTestHandler(webapp2.RequestHandler):
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
    ('/', IndexHandler),
    ('/response', ResponseHandler),
    ('/write', WriteHandler)
], debug=True)
