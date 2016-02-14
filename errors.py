"""Define the possible exceptions that the system can throw."""

class LoginError (Exception):
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