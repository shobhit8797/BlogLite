from application.models import *
from flask import current_app as app
from flask import request, redirect, url_for, render_template, flash
from flask import render_template
from flask_login import login_required, current_user, login_user

@app.route('/signup', methods=['GET'])
def signup():
    if not current_user.is_authenticated:
        return render_template('signup.html')
    else:
        # flash('You are already logged in')
        return redirect(url_for('index'))

@app.route('/login', methods=['GET'])
def login():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        # flash('You are already logged in')
        return redirect(url_for('index'))

# Create a user loader function takes care of reloading the user object from the user ID stored in the session

@app.route('/')
@login_required
def index():
    posts = Post.query.filter(Post.username.in_([user.username for user in current_user.following])).all()
    print(posts)
    return render_template('index.html', posts=posts)


@app.route('/settings', defaults={'active': None})
@app.route('/settings/<active>')
@login_required
def settings(active):
    if active == None:
        active = 'edit_profile'
    return render_template('settings.html', active=active)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template('search.html')


@app.route('/post', methods=['POST'])
def posts():
    if request.method == 'POST':
        content = request.form['post_content']
        author = User.query.filter_by(username = current_user.username).first().username

        post = Post(title=content, username=author)
        db.session.add(post)
        db.session.commit()
        print(User.query.filter_by(username = current_user.username).first().username)
        print('post uploaded sucessfully')
        
        return redirect(url_for("index"))


@app.route('/<username>')
@login_required
def display_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('display_profile.html', user=user)
    else:
        return '''<p>Wrong username entered.... Update this function and make it an error page and give  button to go to search page or index page</p>'''



@app.errorhandler(401)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403