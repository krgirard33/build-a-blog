#!/usr/bin/env python
import webapp2
import jinja2
import os
from google.appengine.ext import db

#set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    """ handles pulling up html pages """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogDB(db.Model):
    """ database of what gets posted """
    title = db.StringProperty(required=True)
    blogtext = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
    """ handles the first page """
    def render_posts(self, title="", blogtext="", error=""):
        blogs = db.GqlQuery("SELECT * FROM BlogDB ORDER BY created DESC LIMIT 5")
        self.render("posts.html", title=title, blogtext=blogtext, error=error, blogs=blogs)

    def get(self):
        self.render_posts()

class NewPost(Handler):
    """ handles the creation of new post """
    def render_newpost(self, title="", blogtext="", error=""):
        blogs = db.GqlQuery("SELECT * FROM BlogDB ORDER BY created DESC LIMIT 5")
        self.render("newpost.html", title=title, blogtext=blogtext, error=error, blogs=blogs)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        blogtext = self.request.get("blogtext")

        if title and blogtext:
            b = BlogDB(title=title, blogtext=blogtext)
            b.put()
            self.redirect("/blog/%s" % b.key().id())
        else:
            error = "We need title and content to post this"
            self.render_newpost(title, blogtext, error)


class SinglePost(Handler):
    """ handles calls for a specific post """
    def render_singlepost(self, title="", blogtext=""):

        self.render("singlepost.html", title=title, blogtext=blogtext)

    def get(self, id):
        b = BlogDB.get_by_id(int(id))
        if b:
            self.render_singlepost(title=b.title, blogtext=b.blogtext)

        else:
            # TODO: Get it to say the ID number
            error = "We looked high and low, but this doesn't  seem to exist"
            self.response.out.write(error)


"""
This function should return a list with at most limit posts in descending order by time created,
and it should start with the post in position offset. For example, if there are 8 posts, get_post(5, 5)
should return posts 6 through 8, by creation time. get_posts(5, 0) should return the 5 most recent posts.

Then refeactor the handler for your main page to call get_posts with the appropriate parameters. Add code
that allows the user to provide a GET query parameter named page that represents that page that they
would like to view. When the user requests /blog?page=1 they should see the 5 most recent posts
(the same as when /blog is requested), when they request /blog?page=2 the next 5 posts should be displayed,
and so on.
"""
# def get_posts(limit, offest):
# TODO: query the database for posts, and return them
    #posts.count(offset=offset, limit=page_size)
    # if page =1 and post count > limit
    # show next
    # elif page > 1 & page count > 1 & post > limit*2
    # then back & next
    # elif page count > 1 & post < limit*2
    # then just back
    # if page count =1 & post > limit
    # then next
    # yeah, making this too convuluted...

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', MainPage),
    webapp2.Route('/blog/<id:\d+>', SinglePost),
    ('/newpost', NewPost)
], debug=True)
