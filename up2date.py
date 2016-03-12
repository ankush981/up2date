from flask import Flask, request, redirect, url_for, abort, render_template, flash
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required
import collections, json
import config
from errors import *
from models import *
from managers import *
from forms import *
from flask.ext.login import login_user, logout_user, LoginManager, current_user
from flask_wtf.csrf import CsrfProtect
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap

# Create the flask app
app = Flask(__name__)
app.config['DEBUG'] = config.DEBUG_MODE
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Wrap it in Bootstrap
Bootstrap(app)

# Wrap the app in login manager from Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'show_home'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Wrap the add in db objects also
# Note: db is defined in models.py
db.init_app(app)

# Add CSRF security
csrf = CsrfProtect()
csrf.init_app(app)

# Make important objects available on Shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

# Wrap shit in a Scrip manager
manager = Manager(app)

# Set up database migration
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))

@app.route('/')
def show_home():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('show_dashboard'))
    login_form = LoginForm()
    reg_form = RegForm()
    return render_template('home.html', login_form = login_form, reg_form = reg_form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('show_dashboard'))
        flash('Invalid email or password')
    reg_form = RegForm()
    return render_template('home.html', login_form = form, reg_form = reg_form)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            LoginManagerOld().register_user(email, password)
        except UserAlreadyExistsError as e:
            flash(e.get_error_message())
            return redirect(url_for('show_home'))
        else:
            flash('Registration successful! You may log in now.')
            return redirect(url_for('show_home'))

#Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def show_dashboard():        
    if current_user is not None and current_user.is_authenticated:
            um = UserManager()
            all_data = um.get_all_websites()
            user_web = um.get_subscriptions(current_user)

            return render_template('dashboard.html', all_data=all_data, subscriptions=user_web)
    return redirect(url_for('show_home'))

# Save route
@app.route('/save', methods=['POST'])
@login_required
def save_subscriptions():
    if request.method == 'POST':
        sites = request.form.get('selected')
        sites = sites[0:-1] # Remove trailing comma
        UserManager().update_subscriptions(session.get('email'), sites)
        flash("Subscriptions updated!")
        return "1"

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_home'))

if __name__ == "__main__":
    manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
    manager.run()