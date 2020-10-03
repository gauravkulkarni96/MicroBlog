from functools import wraps
from app import app
from flask import (session,render_template, redirect, 
                   request, url_for)
from models import db, login_data, post_data

@app.route("/")
def home():
    username=None
    if 'username' in session:
        username = session['username']
        return redirect(url_for('user',username=username))
    return render_template("base.html")

def login_required(f):
    @wraps(f)
    def temp(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return temp

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_data.query.filter_by(username=username).first()
        if user and user.password == password:
            session['logged_in']=username
            session['user_id']=user.user_id
            session['username']=user.username
            return redirect(url_for('user',username=user.username))
        else:
            pass
    return redirect(url_for('home'))


@app.route("/user/<username>")
@login_required
def user(username):
    all_posts =None
    if username == session['logged_in']:
        all_posts = show_post()
        return render_template('user.html',all_posts=all_posts, username = username)
    else:
        return redirect(url_for('error404'))

@app.route('/signup', methods=['POST','GET'])
def signup():
    error = None
    if request.method == 'POST':
        user = login_data(request.form['username'], request.form['password'])
        if login_data.query.filter_by(username=user.username).first():
            error="Username Already exists"
        else:
            db.session.add(user)
            db.session.commit()
    return render_template("base.html",error=error)
#    return redirect(url_for('home',error=error))

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/404')
def error404():
    return render_template('404.html')

@app.route('/post-new', methods = ['POST','GET'])
@login_required
def postnew():
    if request.method == 'POST':
        post = request.form['post']
        title = request.form['title']
        tags = request.form['tags']
        date = request.form['date']
        time = request.form['time']
        user_id = session['user_id']
        save = post_data(post,title,tags,date+' '+time,user_id)
        db.session.add(save)
        db.session.commit()
    return redirect(url_for('home'))

def show_post():
    all_posts = post_data.query.filter_by(user_id= session['user_id']).order_by('-date')
    return all_posts

@app.route('/search', methods = ['POST','GET'])
@login_required
def search():
    results=None
    if request.method == 'POST':
        keyword = request.form['search']
        results = post_data.query.filter_by(tags = keyword, user_id = session['user_id'])
    return render_template('user.html',all_posts=results, username = session['username'])
