from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import collections, json
import config
from errors import *
from models import db #rest of the models are used in managers.py
from managers import *

# Create the flask app
app = Flask(__name__)
app.config['DEBUG'] = config.DEBUG_MODE
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # db was defined in models.py

@app.route('/')
def show_home():
    if 'logged_in' in session and session['logged_in'] == True:
        return redirect(url_for('show_dashboard'))
    elif request.method == 'POST':
        return True
    else:
        return render_template('home.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            LoginManager().check_user(email, password)
        except NoUserFoundError as e:
            flash(e.get_error_message())
            return redirect(url_for('show_home'))
        except LoginError as e:
            flash(e.get_error_message())
            return redirect(url_for('show_home'))
        else:
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('show_dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            LoginManager().register_user(email, password)
        except UserAlreadyExistsError as e:
            flash(e.get_error_message())
            return redirect(url_for('show_home'))
        else:
            flash('Registration successful! You may log in now.')
            return redirect(url_for('show_home'))

@app.route('/dashboard', methods=['GET', 'POST'])
def show_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('show_home'))
    elif session.get('logged_in') == True:
            all_data = UserManager().get_all_websites()
            subscriptions = UserManager().get_subscriptions(session.get('email'))
            if subscriptions:
                subscriptions = subscriptions.split(',')
            else:
                subscriptions = list()
            return render_template('dashboard.html', all_data=all_data, subscriptions=subscriptions)

@app.route('/save', methods=['POST'])
def save_subscriptions():
    if request.method == 'POST':
        sites = request.form.get('selected')
        sites = sites[0:-1] # Remove trailing comma
        UserManager().update_subscriptions(session.get('email'), sites)
        flash("Subscriptions updated!")
        return "1"

@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('email')
    flash('You were logged out')
    return redirect(url_for('show_home'))
