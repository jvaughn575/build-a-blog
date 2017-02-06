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

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/blog")

class BlogHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('base.html')
        content = t.render(blogs="Under Development - See your Blogs Soon!")
        self.response.write(content)

class NewBlogHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('new-blog-form.html')
        content = t.render()
        self.response.write(content)

    def post(self):
        title = self.request.get('title').strip()
        new_post = self.request.get('new_post').strip()

        error_title = ""
        error_new_post = ""

        if not title:
            error_title = "You need to add a title!"
        if not new_post:
            error_new_post = "You need to write your post!"

        if title and new_post:
            self.redirect("/")


        else:
            t = jinja_env.get_template('new-blog-form.html')
            content = t.render(error_title = error_title,
                               error_new_post = error_new_post,
                               title=title,
                               new_post=new_post)
            self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog',BlogHandler),
    ('/blog/newpost',NewBlogHandler)
], debug=True)
