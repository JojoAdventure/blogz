from flask import Flask, request, redirect, render_template
import cgi
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8888/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False
        
posts = []

@app.route('/newpost', methods=['POST', 'GET'])
def NewPost():
    return render_template('newpost.html', title='New Post')

@app.route('/viewpost', methods=['POST', 'GET'])
def ViewPost():
    return render_template('blogpost.html', title='View Post')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blogpost_name = request.form['blogpost']
        new_blogpost = BlogPost(blogpost_name)
        db.session.add(new_blogpost)
        db.session.commit()
        posts.append(new_blogpost)

    return render_template('blog.html',title="Build A Blog", posts=posts)
        
if __name__ == '__main__':
    app.run()