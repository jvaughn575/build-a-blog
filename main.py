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

def get_posts(limit, offset):
    posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC " + "LIMIT " + str(limit) + " OFFSET " + str(offset))
    return posts

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/blog")

class BlogListHandler(webapp2.RequestHandler):
    def get(self):
        limit = 5
        page_number = self.request.get("page")
        blog_entries = get_posts(5,0)
        post_count = blog_entries.count()

        if page_number and int(page_number) >= 2:
            page_number = int(page_number)
            offset = (page_number * limit)-5
            blog_entries = get_posts(limit, offset)
            previous_page = page_number - 1
            page_number += 1
            post_count -= offset
            #self.response.write(page_number)
            t = jinja_env.get_template('display-posts.html')

            if post_count > limit:
                content = t.render(posts = blog_entries,pageturn="<a href='/blog?page=" + str(previous_page) + "'>< prev</a> | <a href='/blog?page=" + str(page_number) + "'>next ></a>")
            else:
                content = t.render(posts = blog_entries,pageturn="<a href='/blog?page=" + str(previous_page) + "'>< prev</a>")
            self.response.write(content)

        else:
            t = jinja_env.get_template('display-posts.html')
            content = t.render(posts = blog_entries, pageturn="<a href='/blog?page=2'>next ></a>")
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
            id = (b.put()).id()
            self.redirect("/blog/" + str(id))

        else:
            t = jinja_env.get_template('new-blog-form.html')
            content = t.render(error_title = error_title,
                               error_body = error_body,
                               title=title,
                               body=body)
            self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        #self.response.write(id)
        post = Post.get_by_id(int(id))
        if post:
            t = jinja_env.get_template('display-posts.html')
            content = t.render(posts = [post])
            self.response.write(content)


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
