"""Define the possible exceptions that the system can throw."""

"""Base class for exceptions in the Up2date system"""
class Up2dateException(Exception):
    def get_error_message(self):
        raise NotImplementedError

"""Classes for handling login"""
class LoginError (Up2dateException):
    def __init__(self, email): # to-do: Define user class
        self.email = email

    def get_error_message(self):
        '''The default error messages. All derived classes must provide their own.'''
        return "Unknown login error for {}. Please retry.".format(self.email)

class NoUserFoundError(LoginError):
    def get_error_message(self):
        return "No user found with email {}".format(self.email)

class WrongPasswordError(LoginError):
    def get_error_message(self):
        return "Wrong email/password for {}. Please recheck login details.".format(self.email)

class UserAlreadyExistsError(LoginError):
    def get_error_message(self):
        return "Sorry, but the email {} is already taken!".format(self.email)