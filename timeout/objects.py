import webapp2
import os
import jinja2
from google.appengine.ext import ndb

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
