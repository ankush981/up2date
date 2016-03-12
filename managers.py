"""Manager classes for Login, Preferences, etc."""
from models import *
from errors import *

class LoginManager:
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
        """Returns all categories in the system having non-zero websites. It is better to return categories than websites because the views expect to render a dictionary keyed by category id"""     
        return [cat for cat in Category.query.order_by(Category.name).all() if cat.websites is not None and len(cat.websites.all()) > 0]

    def get_subscriptions(self, user):
        return user.websites

    def update_subscriptions(self, user, websites):
        if user.websites is None:
            user.wesbites = list()

        for w in websites:
            user.websites.append(w)

        db.session.add(user)
        db.session.commit()