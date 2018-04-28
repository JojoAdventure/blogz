from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:asdf@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, user):
        self.name = name
        self.body = body
        self.user = user

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    user_posts = db.relationship('BlogPost', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.get(int(user_id))
        posts = BlogPost.query.filter_by(user_id=user_id).all()
        return render_template('singleUser.html', user=user, posts=posts, title='asdfasdfadsf')
    
    users = User.query.all()
    return render_template('index.html',title="Build A Blog", users=users)

@app.route('/blog/newpost', methods=['POST', 'GET'])
def NewPost():
    if request.method == 'POST':
        isError = False
        owner = User.query.filter_by(username=session['username']).first()
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
            new_blogpost = BlogPost(title, body, owner)
            db.session.add(new_blogpost)
            db.session.commit()
            posts = BlogPost.query.all()
            post = posts[len(posts)-1]
            return render_template('blogpost.html', post=post)

    return render_template('newpost.html', title='New Post')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = BlogPost.query.get(int(post_id))
        return render_template('blogpost.html', post = post, title='asdfasdfadsf')
    
    posts = BlogPost.query.all()
    return render_template('blog.html',title="Build A Blog", posts=posts)

@app.route('/blog/signup', methods=['POST', 'GET'])        
def signup():
    if request.method == 'POST':
        isError = False
        username = request.form['username']
        password = request.form['password']
        password_verify = request.form['verify']

        params = dict(username = username)

        if not bool(re.match(r"^[a-zA-Z0-9_-]{3,20}$", username)):
            params['uerror'] = "Invalid Username"
            isError = True
        
        if not bool(re.match(r"^.{3,20}$", password)):
            params['perror'] = "Invalid Password"
            isError = True

        if password != password_verify or password_verify == '':
            params['verror'] = "Passwords do not match"
            isError = True

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
        else:
            params['uerror'] = "Existing username"
            isError = True

        if isError:
            return render_template('signup.html', **params)
        else:
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog/newpost')

    return render_template('signup.html', title='asdhgkashdgkljahsdlkgjhasdkjgagkjhdkgjdh')

@app.before_request
def require_login():
    allowed_routes = ['signup', 'login', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/blog/login')

@app.route('/blog/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        params = dict(username=username)
        user = User.query.filter_by(username=username).first()
        if not user:
            params['uerror'] = "User does not exist here have a login page"
            return render_template('signup.html', **params)
        else:
            if user and user.password == password:
                session['username'] = username
                flash("Logged in")
                return redirect('/blog/newpost')
            else:
                flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/blog/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()