"""Manager classes for Login, Preferences, etc."""
from models import *
from errors import *
from collections import OrderedDict

class LoginManager:
    def check_user(self, email=None, password=None):
        import sys
        
        user = User.query.filter_by(email=email, password=password).first()

        if not user:
            raise NoUserFoundError(email)

        return True

    def register_user(self, email=None, password=None):
        user = User.query.filter_by(email=email, password=password).all()

        if len(user) > 0:
            raise UserAlreadyExistsError(email)

        user = User()
        user.email = email
        user.password = password

        db.session.add(user)
        db.session.commit()

        return True

class UserManager:
    """Class that manages preferences, subscriptions, etc."""
    def get_all_websites(self):
        all_data = OrderedDict()
        categories = Category.query.all()

        # Produce an ordered dict with keys are cateogry names, so that these can
        # rendered in exactly the same order in the view        
        for cat in categories:
            web = cat.websites.all()
            if web:
                if cat.name in all_data:
                    all_data[cat.name].append(web)
                else:
                    all_data[cat.name] = web
        
        return all_data

    def get_subscriptions(self, email):
        return User.query.filter_by(email=email).first().sites

    def update_subscriptions(self, email, sites):
        user = User.query.filter_by(email=email).first()
        user.sites = sites
        db.session.add(user)
        db.session.commit()