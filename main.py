from flask import Flask, request, redirect, render_template
import cgi
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, name, body):
        self.name = name
        self.body = body

@app.route('/blog/newpost', methods=['POST', 'GET'])
def NewPost():
    if request.method == 'POST':
        isError = False
        title = request.form['post_title']
        body = request.form['post_body']
        terror = ''
        berror = ''

        if title == '':
            terror = "Type something will ya!"
            isError = True
        if body == '':
            berror = "Type something will ya!"
            isError = True

        if isError:
            return render_template('newpost.html', terror=terror, berror=berror, post_title=title, body=body)
        else:
            new_blogpost = BlogPost(title, body)
            db.session.add(new_blogpost)
            db.session.commit()
            posts = BlogPost.query.all()
            last = posts[len(posts)-1]
            return redirect('/blog?id=' + str(last.id))

    return render_template('newpost.html', title='New Post')

@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = BlogPost.query.get(int(post_id))
        return render_template('blogpost.html', post = post, title='asdfasdfadsf')
    
    posts = BlogPost.query.all()
    return render_template('blog.html',title="Build A Blog", posts=posts)
        
if __name__ == '__main__':
    app.run()