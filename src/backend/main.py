# Runs Instajawn

from pathlib import Path
import os

# helper
from helper.account import Account

# executable sequence for instajawn
from x import Runner


'''File Paths'''
ROOT_PATH = Path( os.getcwd() ) # current working directory in Path form of your OS system

'''Account Information'''
USERNAME = 'broda.care'
PASSWORD = 'Lollypop99!'

'''FILE NAMES'''
HASHTAG_FILE = 'broda_hashtags.txt'


if __name__ == '__main__':

    my_account = Account(user=USERNAME, password=PASSWORD) 

    my_jawn = Runner(account=my_account, root_path=ROOT_PATH, hashtag_file=HASHTAG_FILE) # InstaJawn session

    my_jawn.run() # Instajawn is ready for prime time