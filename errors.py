"""Define the possible exceptions that the system can throw."""

"""Base class for exceptions in the Up2date system"""
class Up2dateException(Exception):
    def get_error_message(self):
        raise NotImplementedError


"""Classes for handling login"""
class LoginError (Up2dateException):
    def __init__(self, user): # to-do: Define user class
        self.user = user

    def get_error_message(self):
        '''The default error messages. All derived classes must provide their own.'''
        return "Unknown login error for email {}. Please retry.".format(self.user.email)

class NoUserFoundError(LoginError):
    def get_error_message(self):
        return "No user found with email {}".format(self.user.email)

class WrongPasswordError(LoginError):
    def get_error_message(self):
        return "Wrong email/password for {}. Please recheck login details.".format(self.user.email)

"""Exceptions for DB access"""
class DBError(Up2dateException):
    def get_error_message(self, db):
        return "Unknown database error"

class DBConnectError(DBError):
    def get_error_message(self, db):
        return "Couldn't connect to DB using these credentials: Host = {}, Username = {}, Password = {}, DB name = {}".format(db.host, db.username, db.passwd, db.dbname)