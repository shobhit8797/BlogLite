from application.models import *
from flask import current_app as app
from flask import request,redirect,url_for,render_template,flash
from flask import render_template


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        # Get the form data
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phn = request.form['phn']
    
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            # flash('Username already exists')
            return redirect(url_for('signup'))
        # Create new user
        new_user = User(username=username, password=password, name=name, email=email, phn=phn)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                # login_user(user)
                return redirect(url_for('index'))
            else:
                # flash('Incorrect password')
                return redirect(url_for('login'))
        else:
            flash('Username does not exist')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


# Create a user loader function takes care of reloading the user object from the user ID stored in the session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings', defaults={'active': None})
@app.route('/settings/<active>')
def settings(active):
    if active == None:
        active = 'profile'
    return render_template('settings.html', active=active)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phn = request.form['phn']
        user = User.query.filter_by(username=username).first()
        if user:
            user.password = password
            user.name = name
            user.email = email
            user.phn = phn
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            # flash('Username does not exist')
            return redirect(url_for('edit_profile'))
    else:
        return render_template('settings.html')