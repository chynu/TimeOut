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
        template = jinja_environment.get_template('templates/index_v2.html')
        current_user = users.get_current_user()
        if current_user: # if logged in
            logging.info("Logged in!")
            user_id = current_user.user_id()
            #looks for user in database
            user_identification = User.query().filter(User.email_user_id == user_id)

            log = users.create_logout_url('/')
            nick = current_user.nickname()
            log_text = "log out"
            dash_text = "Dashboard"

            #if the user is not in the database after logging in.....
            if not user_identification.get():
                logging.info("Logged in, but not in database.")
                current_user = User(
                    name = current_user.nickname(),
                    email = current_user.email(),
                    email_user_id = user_id
                )
                #...logs you in and redirects you to basic info where you can create your instance in the database
                # log = users.create_login_url('/')
                # nick = ""
                # log_text = "Log in"
                # dash_text = ""
                current_user.put()

        else:
            logging.info("Not logged in!")
            log = users.create_login_url('/')
            nick = "Anonymous"
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
        current_user = users.get_current_user()
        if current_user:
            nick = current_user.nickname()
            log = users.create_logout_url('/')
            log_text = "log out"
            dash_text = "dashboard"
        else:
            nick = "Anonymous"
            log = users.create_login_url('/')
            log_text = "log in"
            dash_text = ""

        # fetch list of all compliments, get random compliment in entire list;
        #    also store ID of this compliment for future use.
        comp_list = Compliment.query().filter(Compliment.comp_type == self.request.get("feeling")).fetch()
        logging.info(comp_list)
        chosen_comp = comp_list[random.randint(0, ( len(comp_list)-1 ))]
        temp = {
            "compliment": chosen_comp.content,
            "comp_id": chosen_comp.key.id(),
            "username": nick,
            "log_url": log,
            "log_text": log_text,
            "dash_text": dash_text
        }
        self.response.write(template.render(temp))

    def post(self):
        template = jinja_environment.get_template('templates/response_confirm.html')
        logging.error(self.request.get("points"))
        logging.error(str(self.request.get("points") < 0))

        if(int(self.request.get("points")) < 0):
            updated_comp = Compliment.get_by_id(int(self.request.get("id"))).report()
        else:
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
        current_user = users.get_current_user()

        if current_user:
            nick = current_user.nickname()
            log = users.create_logout_url('/')
            log_text = "log out"
            dash_text = "dashboard"
        else:
            nick = "Anonymous"
            log = users.create_login_url('/')
            log_text = "log in"
            dash_text = ""

        temp = {
            "username": nick,
            "log_url": log,
            "log_text": log_text,
            "dash_text": dash_text
        }
        self.response.write(template.render(temp))

    def post(self):
        current_user = users.get_current_user()
        new_compliment = self.request.get('words')
        complimentObj = Compliment(content=new_compliment,points=0,views=0, comp_type = self.request.get('emotion'), reported = False) #,allow_multiple = True))
        comp_key = complimentObj.put()

        if current_user: #if logged in, then add to that user's comp list. if not, don't add it to anything.
            matched_user = User.query().filter(User.email_user_id == current_user.user_id()).get()
            logging.warning(str(matched_user))
            matched_user.compliment_list.append(comp_key)
            matched_user.put()
            nick = current_user.nickname()
            log = users.create_logout_url('/')
            log_text = "log out"
            dash_text = "dashboard"
        else:
            nick = "Anonymous"
            log = users.create_login_url('/')
            log_text = "log in"
            dash_text = ""

        template = jinja_environment.get_template('templates/write_confirm.html')
        temp = {
            "username": nick,
            "log_url": log,
            "log_text": log_text,
            "dash_text": dash_text
        }
        self.response.write(template.render(temp))

""" HANDLER INFORMATION
    url: /dashboard
    handler: DashHandler
    frontend: /templates/dashboard.html,        /stylesheets/dashboard.css  """
class DashHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/dashboard.html')
        current_user = users.get_current_user()

        # if a not-logged in person tries to go to /dashboard, they will redirect to homepage.
        if not current_user:
            self.redirect('/')
        else:
            user_id = current_user.user_id()
            matched_user = User.query().filter(User.email_user_id == user_id)
            logging.error(matched_user.get())
            temp = {
                "fetched_list": Compliment.query().fetch(), #all compliments.
                "user_list": matched_user.get().compliment_list, # list of compliment keys (specific to user)
                "username": current_user.nickname(),
                "log_url": users.create_logout_url('/'),
                "log_text": "log out",
                "dash_text": "dashboard"
            }
            self.response.write(template.render(temp))

# ================ OBJECTS =================
# user object, for each login. ONLY instantiated when a person logs in with gmail username.
class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    compliment_list = ndb.KeyProperty("Compliment", repeated=True)
    email_user_id = ndb.StringProperty(required=True)

# compliment object, created every time someone WRITES a compliment.
# called every time someone ASKS FOR a compliment.
class Compliment(ndb.Model):
    content = ndb.StringProperty(required=True)
    points = ndb.IntegerProperty(required=True)
    views = ndb.IntegerProperty(required=True)
    comp_type = ndb.StringProperty(required = False)
    reported = ndb.BooleanProperty(required = True)

    def addPoints(self, inc):
        self.points += inc
        self.views += 1
        return self

    def report(self):
        self.reported = True
        self.views += 1
        return self

# ============== LINKS ===============
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/response', ResponseHandler),
    ('/write', WriteHandler),
    ('/dashboard', DashHandler)
], debug=True)
