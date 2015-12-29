# Up2date
Makes following your favorite websites a snap!

In a hurry? Go straight to the [app](http://plainsight.in:5000).

### Technologies used

Up2date is built on:

* Python 3.4
* Flask 0.10.0
* BeautifulSoup 4
* MySQL
* Bootstrap

#### Too many websites to track?

Up2date was created to solve a problem I was facing: tracking multiple websites. There are over a dozen websites I love, but I don't always have the leisure to visit each one of them (if I can remember all of them, that is!). Wouldn't it be nice, I said to myself one day, if someone could comb through them and send me an email summary of just the stuff that matters? Bingo! Up2date was born.

***Caveat:* No solution is perfect, and Up2date is the same. The downside here is that adding a new website means examining its structure and adding a class to the system.**

The app is running [here](http://plainsight.in:5000) (please do not bookmark &ndash; I'll be changing the links soon).

#### Installation instructions

* Paste the code in a directory of your choice.
* Set up a virtual environment and install the required packages (look at the import statemtns in up2date.py and scraper/scraper.py).
* Set up the DB (covered later)
* Create db_details.py having the four fields containing DB credentials:
```
host = 'localhost'
user = 'root'
passwd = 'xxxx'
dbname = 'up2date'
```
* Finally, the script scraper/scraper.py needs to be set up as a cron job, respecting the virtualenv.

##### DB setup

The DB should contain the following three tables.
```
mysql> desc users;
+----------+---------------+------+-----+---------+-------+
| Field    | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| email    | varchar(100)  | NO   | PRI |         |       |
| password | varchar(100)  | NO   |     | NULL    |       |
| name     | varchar(200)  | YES  |     | NULL    |       |
| sites    | varchar(5000) | YES  |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+

mysql> desc categories;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | smallint(6)  | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | YES  |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

mysql> desc websites;
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| id          | int(11)       | NO   | PRI | NULL    | auto_increment |
| name        | varchar(100)  | NO   |     | NULL    |                |
| category_id | smallint(6)   | YES  | MUL | NULL    |                |
| url         | varchar(1000) | YES  |     | NULL    |                |
| class_name  | varchar(50)   | NO   |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+
```
Please note:
* `category_id` in `websites` has a foreign key constraint.
* `sites` in `users` holds the ids of subscriptions as a comma-separated string. So, if I subscribe to site ids 1, 4 and 5, my `sites` field would contain `1,4,5` (as a string, of course).

#### Wish list

Up2date was coded in a passionate hurry, so it lacks many things that I'll be adding subsequently:
* Have at least 50 important websites crawled daily.
* Validating email addresses of new registrations.
* Option of individual mail and digest.
* Allowing users to set up different alert times.
* Make the code base fully object-oriented (migrate to Django, if need be)
