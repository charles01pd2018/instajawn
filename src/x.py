# Runner for combining the instajawn sequences


from time import sleep
from pathlib import Path

# helper
from helper.prompt import prompt_user, prompt_pass
from helper.account import Account


# sequences
from sequence.hashtag import go_through_tags
from sequence.feed import like_feed

from instajawn import InstaJawn


class Runner:

    def __init__(self, account: Account, root_path: Path, hashtag_file: str, continuous: bool=True, sleep_time: int=4):
        '''Initializes class varaibles'''

        '''
            account: represents the Instagram account for the user with paramenters user and password
            root_path: root path of the instajawn program
            hashtag_file: hashtags .txt file containing the hashtags to go through
            continuous: True = the program continuously runs in the background, False = session ends after amount of posts liked is acheived
            sleep_time: time InstaJawn sleeps before starting next session if program is continuous 
        '''

        if account.user == '' or account.password == '': # Prompt the user
            self.instance = InstaJawn(prompt_user(), prompt_pass(), root_path=root_path, headless=True) # Instagram session

        else: # Start the session
            self.instance = InstaJawn(account.user, account.password, root_path=root_path, headless=True) 

        self.hashtag_file = hashtag_file 

        self.continuous = continuous 
        
        self.sleep_time = sleep_time 

    
    def run(self):
        '''Runs InstaJawn'''

        while True:
            go_through_tags(insta_session=self.instance, hashtag_file_name=self.hashtag_file) # Runs hashtag sequence
            # like_feed(insta_session=self.instance) # Likes posts on an Instagram feed
            
            if self.continuous == True:
                sleep(self.sleep_time) # InstaJawn takes a break
            
            else: 
                self.instance.driver.quit() # Quits Chrome Driver
                exit() # Exits the program