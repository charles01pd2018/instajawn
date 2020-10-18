# Runs Instajawn

from x import Runner
from helper.account import Account


'''File Paths'''
ROOT_PATH = ''

'''Account Information'''
USERNAME = ''
PASSWORD = ''

'''FILE NAMES'''
HASHTAG_FILE = ''


if __name__ == '__main__':

    my_account = Account(user=USERNAME, password=PASSWORD) 

    my_jawn = Runner(account=my_account, root_path=ROOT_PATH, hashtag_file=HASHTAG_FILE) # InstaJawn session

    my_jawn.run() # Instajawn is ready for prime time