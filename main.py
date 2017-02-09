#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


'''class NewPostHandler(db.Model):
    title = db.StringProperty(required = True)
    new_post = db.TextProperty(required = True)
    created_on = db.DateTimeProperty(auto_now_add = True)


class ViewPostHandler(webapp2.RequestHandler):

    def get(self, id):
        pass #relace this with some code to handle the request
        # to get post number 6
        # Once you have set up this new dynamic route, and the corresponding handler and get method, 
        # you are ready to do a simple test. In the get method, simply print the value of the id 
        # parameter to the response. No need to use a template, or even any HTML, just 
        # self.response.write(). Then visit such a route in your browser (e.g. /blog/42). '''

class MainHandler(Handler):
    def get(self):
        #self.write("Word")
        # items = self.request.get_all("food")
        self.render("index.html")
    
    def post(self):
        title = self.request.get("title")
        

'''class LoginHandler(Handler):
    def get(self):
        # items = self.request.get_all("food")
        self.render("login.html")

class SingUpHandler(Handler):
    def get(self):
        template = jinja_environment.get_template("signup.html")
        self.response.out.write(template.render())

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")


class WelcomeHandler(Handler):
    def get(self):
        # items = self.request.get_all("food")
        self.render("welcome.html")


class NewPostHandler(Handler):
    def get(self):
        # items = self.request.get_all("food")
        self.render("newpost.html")'''

app = webapp2.WSGIApplication([
    ('/', MainHandler,
    '''"/blog", LoginHandler,
    "/newpost", NewPostHandler,
    "/blog/<id:\d+>", VeiwPostHandler''')
], debug=True)
