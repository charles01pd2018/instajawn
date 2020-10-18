# Likes posts on an Instagram Feed

from instajawn import InstaJawn

from random import randint
from time import sleep

# Constants

'''Limits'''
NUM_POSTS = randint(40, 61) # Number of posts to go through


def like_feed(insta_session: InstaJawn, num_posts: int=NUM_POSTS, wait_time: int = randint(2,4)) -> None: 
    '''Goes through feed and likes posts'''

    '''
        insta_session: current InstaJawn selenium chrome browser session
        num_posts: number of posts to go through and like
        wait_time: amount of time to wait in between post likes
    '''

    for post in range(num_posts): 
        try: # When the like is visible on the screen
            insta_session.driver.like_post() 

        except: # The like button is not visible on the screen
            pass # Keeps the program going

        insta_session.driver.execute_script("window.scrollBy(0, 20);") # Scroll the page 

        sleep(wait_time) # Waits for the page to finish scrolling before liking the next post


    insta_session.store_num_likes('FEED') # Stores the number of likes performed in the session
    insta_session.nav_home_screen() # Goes back to the home screen