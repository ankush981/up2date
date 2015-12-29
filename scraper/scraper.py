"""
The main scraper cron. The job of this script is to read all users' data from the DB, compile the necessary newsletters, and mail them. It works intelligently, crawling only those websites that have at least one subscription. 
"""
import MySQLdb, MySQLdb.cursors
import os, os.path, sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import db config from previous directory
sys.path.insert(0, '..')
import db_config

# Read paths in relation to this file's directory, not the pwd
this_dir = os.path.dirname(os.path.realpath(__file__))

# The db and cursor objects
db = None
cursor = None

# location of HTML files of each website scraped today
html_file_dir = this_dir + os.sep + 'classes' + os.sep + 'data'

# Connect to DB
try:
    db = MySQLdb.connect(host=db_config.host, user=db_config.user, passwd=db_config.passwd, db=db_config.dbname, cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
except Exception as e:
    print("Something horrible occurred!")
    print(e)

# Get details of websites with non-zero subscriptions
cursor.execute('SELECT sites FROM users')
rows = cursor.fetchall()

# Set whose members are website ids with > 0 subscriptions. 
websites = set()

for row in rows:
    row = row["sites"] 
    row = row.split(',') # Collect all comma-separated value in list
    for r in row:
        websites.add(r) # Add to set - will discard duplicates

# Dictionary to hold all data - keys are website id
html_of_websites = dict()

for site_id in websites:
    cursor.execute('SELECT url, class_name FROM websites WHERE id = %s', [site_id])
    row = cursor.fetchone()
    
    url = row['url']
    class_name  = row['class_name']
    module_name = class_name.lower()

    # import the module dynamically
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './classes')))
    module = __import__(module_name)

    instance = getattr(module, class_name)(dirname=html_file_dir, filename=module_name, url=url)

    # finally, save site html in the master dictionary
    html_of_websites[site_id] = instance.getSummary()

# Now get individual mailers and send summary
cursor.execute('SELECT email, sites FROM users')
users = cursor.fetchall()

body_start = "<html><head></head><body>Here are your updates: <br>"
body_end = "<br><br>Have fun,<br>Ankush from Plainsight</body></html>"

from_addr = 'ankush@plainsight.in'
smtpObj = smtplib.SMTP('localhost')

for user in users:
    to_addr = user['email']
    sites = user['sites'].split(',')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your updates from Up2date'
    msg['To'] = to_addr
    msg['From'] = from_addr

    html = ''
    html += body_start

    # Add HTML for all subscriptions
    for site in sites:
        html += '<br>' + html_of_websites[site]

    html += body_end

    html = MIMEText(html, 'html')
    msg.attach(html)

    smtpObj.sendmail(from_addr, [to_addr], msg.as_string())

cursor.close()
smtpObj.quit()
