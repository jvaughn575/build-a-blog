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
import os
import webapp2
import jinja2

# import Google datastore db
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/blog")

class BlogListHandler(webapp2.RequestHandler):
    def get(self):
        blog_entries = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template('display-blog.html')
        content = t.render(posts=blog_entries)
        self.response.write(content)

class NewBlogHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('new-blog-form.html')
        content = t.render()
        self.response.write(content)

    def post(self):
        title = self.request.get('title').strip()
        body = self.request.get('body').strip()

        error_title = ""
        error_body = ""

        if not title:
            error_title = "You need to add a title!"
        if not body:
            error_body = "You need to write your post!"

        if title and body:
            b = Post(title = title, body = body)
            b.put()
            self.redirect("/")


        else:
            t = jinja_env.get_template('new-blog-form.html')
            content = t.render(error_title = error_title,
                               error_body = error_body,
                               title=title,
                               body=body)
            self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        self.response.write(id)


# Make Blog model class
class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog',BlogListHandler),
    ('/blog/newpost',NewBlogHandler),
    webapp2.Route(r'/blog/<id:\d+>', ViewPostHandler),
], debug=True)
