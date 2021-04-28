#flash- allows import for passing a messag when incorrect sign up datails
from flask import Blueprint, render_template, request, flash, redirect, url_for
#import the user we created in models.py
from .models import User
#importing tools that allow us to hash the passowrd
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
#flasklogin package allows us to access and use info for currently logged in user
from flask_login import login_user, login_required, logout_user, current_user


# define this file is a blueprint of app, aka has a bunch of routes inside it, bunch of urls defined
auth = Blueprint('auth', __name__) # setup blueprint for flask app


#assign post requests ', methods=['Get', 'post'...]..., by default only get requests accepted
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #checking if user email sent to us is valid, in db, query db
        user = User.query.filter_by(email=email).first() #first as there could be one but should not be more since each email should be unique
        #if passwords are the same then login
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #true, flask will remember user was logged in
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect. Try again please', category='error')
        else:
            flash('Email does not exist', category='error')    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
#making sure you can only logout if you are logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up' , methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  #collecting data from sign up page
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #requirements for what is accepted when signing up
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 charachters', category='error')
        else:
            #add the user to data 
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))#sha256 is a hashing algo(diff1couldbepicked)
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            #users data added now return them to the homepage, redirect them to a url
            return redirect(url_for('views.home')) #best to use urlfor w/ blueprint name and function name incase root for url is changed


        
    return render_template("sign_up.html", user=current_user)