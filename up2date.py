from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import MySQLdb
import MySQLdb.cursors
import collections, json
import db_config

# Configuration
DEBUG          = True
SECRET_KEY     = '\xc6)\x0f\\\xc5\x86*\xd7[\x92\x89[\x95\xcfD\xfd\xc1\x18\x8e\xf1P\xf7_\r'

# Create the flask app
app = Flask(__name__)
app.config.from_object(__name__)

# Function to connect to DB
def connect_db():
    return MySQLdb.connect(host=db_config.host, user=db_config.user, passwd=db_config.passwd, db=db_config.dbname, cursorclass=MySQLdb.cursors.DictCursor)

# define functions that will make DB available automatically on each request
@app.before_request
def before_request():
    g.db = connect_db()
    g.cursor = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    g.cursor.close()

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
        g.cursor.execute('SELECT email, password FROM users WHERE email = %s', [request.form['email']])
        row = g.cursor.fetchone()

        if not row:
            flash('No such user exists!')
            return redirect(url_for('show_home'))
        elif request.form['password'] == row['password']:
            session['logged_in'] = True
            session['email'] = row['email']
            return redirect(url_for('show_dashboard'))
        else:
            flash('Wrong password / login error.')
            return redirect(url_for('show_home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = g.cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', [email, password])
        g.db.commit()
        flash('Registration successful! You may log in now.')
        return redirect(url_for('show_home'))

@app.route('/dashboard', methods=['GET', 'POST'])
def show_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('show_home'))
    else:
        if session['logged_in'] == True:
            # Get all possible sites
            g.cursor.execute('SELECT C.name AS category_name, W.id AS website_id, W.name AS website_name, W.url AS website_url FROM categories C INNER JOIN websites W ON C.id = W.category_id ORDER BY C.name, W.name')
            all_websites = g.cursor.fetchall()

            # transform these rows of dicts into a single dict, keyed by category name
            all_data = collections.OrderedDict()
            
            for w in all_websites:
                key = w['category_name']
                # if key already exits, add a new row
                if not key in all_data:
                    all_data[key] = list()
                all_data[key].append([w['website_id'], w['website_name'], w['website_url']])

            # Get subscribed sites
            g.cursor.execute('SELECT sites FROM users WHERE email = %s', [session.get('email')])
            subscriptions = g.cursor.fetchone()
            subscriptions = subscriptions['sites'].split(',')
            return render_template('dashboard.html', all_data=all_data, subscriptions=subscriptions)

@app.route('/save', methods=['POST'])
def save_subscriptions():
    if request.method == 'POST':
        sites = request.form.get('selected')
        sites = sites[0:-1]        
        g.cursor.execute('UPDATE users SET sites = %s WHERE email = %s', [sites, session.get('email')])
        g.db.commit()
        flash("Subscriptions updated!")
        return "1"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('You were logged out')
    return redirect(url_for('show_home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
