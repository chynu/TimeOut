import webapp2
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import random
import logging

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
        user = users.get_current_user()
        if user: # if logged in
            log = users.create_logout_url('/')
            nick = user.nickname()
            log_text = user.given_name()
            dash_text = "Dashboard"


            new_user = User(user.nickname, user.email(), )
        else:
            log = users.create_login_url('/')
            nick = ""
            log_text = "Log in"
            dash_text = ""

        temp = {
            "username": nick,
            "log_url": log,
            "log_text": log_text,
            "dash_text": dash_text
        }
        self.response.write(template.render(temp))

""" HANDLER INFORMATION
    url: /response
    handler: ResponseHandler
    frontend: /templates/response.html,         /stylesheets/response.css
              /templates/response_confirm.html, /stylesheets/repsonse.css   """
class ResponseHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/response.html')

        # fetch list of all compliments, get random compliment in entire list;
        #    also store ID of this compliment for future use.
        comp_list = Compliment.query().fetch()
        chosen_comp = comp_list[random.randint(0, ( len(comp_list)-1 ))]
        temp = {
            "compliment": chosen_comp.content,
            "comp_id": chosen_comp.key.id()
        }
        self.response.write(template.render(temp))

    def post(self):
        template = jinja_environment.get_template('templates/response_confirm.html')
        updated_comp = Compliment.get_by_id(int(self.request.get("id"))).addPoints(int(self.request.get("points")))
        updated_comp.put()

        temp = {
            # "test": updated_comp,
            "compliment": updated_comp.content
        }
        self.response.write(template.render(temp))

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
    frontend: /templates/dashboard.html,        /stylesheets/dashboard.css  """
class DashHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/dashboard.html')
        temp = {
            "fetched_list": Compliment.query().fetch()
        }
        self.response.write(template.render(temp))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/login.html')
        self.response.write(template.render())

class TestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index_v2.html')
        self.response.write(template.render())

# ================ OBJECTS =================
# user object, for each login. ONLY instantiated when a person logs in with gmail username.
class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    compliment_list = ndb.ListProperty( required = True)

# compliment object, created every time someone WRITES a compliment.
# called every time someone ASKS FOR a compliment.
class Compliment(ndb.Model):
    content = ndb.StringProperty(required=True)
    points = ndb.IntegerProperty(required=True)
    views = ndb.IntegerProperty(required=True)

    def addPoints(self, inc):
        self.points += inc
        # logging.error("Incremented by " + str(inc))
        self.views += 1
        # logging.error("View added by 1")
        # logging.error(str(self))
        return self

# ============== LINKS ===============
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/response', ResponseHandler),
    ('/write', WriteHandler),
    ('/dashboard', DashHandler),
    ('/login', LoginHandler),
    ('/test', TestHandler)
], debug=True)
