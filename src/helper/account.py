# Represent an account for a user

class Account:

    def __init__(self, user: str, password: str):
        '''Initializes class variables'''
        
        '''
            user: username for the account
            password: password for the account
        '''

        self.user = user
        self.password = password
