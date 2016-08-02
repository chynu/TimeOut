import webapp2
import os
import jinja2
from google.appengine.ext import ndb
import random

jinja_environment = jinja2.Environment(loader =
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

# ================== HANDLERS ====================
""" HANDLER INFORMATION
    url: /
    handler: IndexHandler
    frontend: /templates/index.html,            /stylesheets/index.css     """
class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

""" HANDLER INFORMATION
    url: /response
    handler: ResponseHandler
    frontend: /templates/response.html,         /stylesheets/response.css
              /templates/response_confirm.html, /stylesheets/repsonse.css   """
class ResponseHandler(webapp2.RequestHandler):
    comp_list = Compliment.query().fetch()
    chosen_comp = comp_list[random.randint(0, ( len(comp_list)-1 ))]

    def get(self):
        template = jinja_environment.get_template('templates/response.html')
        # added_points = int(self.request.get('points'))
        # this is where you would query and fetch a list of all compliments, then get a random item from that list.
        temp = {
            "compliment": chosen_comp.content
        }
        self.response.write(template.render(temp))

    def post(self):
        template = jinja_environment.get_template('templates/response_confirm.html')
        global chosen_comp
        chosen_comp.addPoints(self.response.get("points"))
        self.response.write(template.render())

""" HANDLER INFORMATION
    url: /write
    handler: WriteHandler
    frontend: /templates/write.html,            /stylesheets/write.css
              /templates/write_confirm.html     /stylesheets/write.css      """
class WriteHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/write.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/write_confirm.html')
        self.response.write(template.render())
        new_compliment = self.request.get('words')
        complimentObj = Compliment(content=new_compliment,points=0,views=0)
        comp_key = complimentObj.put()

""" HANDLER INFORMATION
    url: /dashboard
    handler: DashHandler
    frontend: /templates/dashboard.html,        /stylesheets/dashboard.css     """
class DashHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/dashboard.html')
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

    def addPoints(self,inc):
        self.points += inc


# ============== LINKS ===============
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/response', ResponseHandler),
    ('/write', WriteHandler),
    ('/dashboard', DashHandler)
], debug=True)
