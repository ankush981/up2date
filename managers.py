"""Manager classes for Login, Preferences, etc."""
from models import *
from errors import *
from flask.ext.login import current_user

class RegistrationManager:
    def register_user(self, email=None, password=None):
        user = User.query.filter_by(email=email, password=password).all()

        if len(user) > 0:
            raise UserAlreadyExistsError(email)

        user = User()
        user.email = email
        user.password = password
        user.role_id = 1

        db.session.add(user)
        db.session.commit()

        return True

class UserManager:
    """Class that manages preferences, subscriptions, etc."""
    def get_all_websites(self):
        """Returns all categories in the system having non-zero websites. It is better to return categories than websites because the views expect to render a dictionary keyed by category id"""     
        return [cat for cat in Category.query.order_by(Category.name).all() if cat.websites is not None and len(cat.websites.all()) > 0]

    def get_subscriptions(self, user):
        return user.websites

    def update_subscriptions(self, web_ids):
        for w_id in web_ids:
            w = Website.query.filter_by(id=w_id).one()
            current_user.websites.append(w)

        db.session.add(current_user)
        db.session.commit()