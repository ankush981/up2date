# Up2date
Makes following your favorite websites a snap!

In a hurry? Go straight to the [app](http://up2date.plainsight.in).

### Technologies used

Up2date is built on:

* Python 3.4
* Flask
* Flask SQLAlchemy
* BeautifulSoup 4
* MySQL
* Bootstrap

#### Too many websites to track?

Up2date was created to solve a problem I was facing: tracking multiple websites. There are over a dozen websites I love, but I don't always have the leisure to visit each one of them (if I can remember all of them, that is!). Wouldn't it be nice, I said to myself one day, if someone could comb through them and send me an email summary of just the stuff that matters? Bingo! Up2date was born.

***Caveat:* No solution is perfect, and Up2date is the same. The downside here is that adding a new website means examining its structure and adding a class to the system.**

The app is running [here](http://up2date.plainsight.in).

#### Installation instructions

* Paste the code in a directory of your choice.
* Set up a virtual environment
* Install the required pip packages from requirements.txt
* Set up the DB (covered later)
* Create `config.py` having the following:
```
DATABASE_URI = 'mysql://user:pass@localhost/up2date'
DEBUG_MODE = True
APP_SECRET_KEY = 'Secret key here'
```
* Finally, the script `scraper/scraper.py` needs to be set up as a cron job, respecting the virtualenv.

##### DB setup

The DB schema can be determined easily by looking into `models.py`.

Please note:
* `category_id` in `websites` has a foreign key constraint.
* `sites` in `users` holds the ids of subscriptions as a comma-separated string. So, if I subscribe to site ids 1, 4 and 5, my `sites` field would contain `1,4,5` (as a string, of course).

#### Wish list

Up2date was coded in a passionate hurry, so it lacks many things that I'll be adding subsequently:
* Have at least 50 important websites crawled daily.
* Validating email addresses of new registrations.
* Option of individual mail and digest.
* Allowing users to set up different alert times.
* Make the code base more object-oriented (now only the scraper part isn't object-oriented)