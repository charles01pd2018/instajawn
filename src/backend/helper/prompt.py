# Prompts user for login credentials

from getpass import getpass

def prompt_user() -> str:
    '''Prompts for username and returns it'''

    return input('Enter the username for your IG: ').strip()
    
def prompt_pass() -> str:
    '''Prompts for password and returns it'''

    return getpass('Enter the password for your IG (The password will not show when you type): ').strip()