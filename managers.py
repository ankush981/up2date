"""Manager classes for Login, Preferences, etc."""
from db import *
from errors import *

class LoginManager:
    def perform_login(self, email=email, password=password):
        user = User.query.filter_by(email=email, password=password)

        if not user:
            raise NoUserFoundError(email)

        return True

    def register_user(self, email=email, password=password):
        user = User.query.filter_by(email=email, password=password)

        if len(user) == 1:
            raise UserAlreadyExists(email)

        user = User()
        user.email = email
        user.password = password

        db.session.add(user)
        db.session.commit()

        return True