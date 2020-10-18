# Instagram Bot Base Class

from selenium import webdriver
from time import sleep
from random import randint, shuffle
from datetime import datetime


class InstaJawn:

    # Class Initialization

    def _initialize_paths(self) -> None:
        '''Initializes Instagram HTML element paths'''

        self._LOGIN_BUTTON = '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]/button/div'
        self._SAVE_INFO_BUTTON = '/html/body/div[1]/section/main/div/div/div/div/button' # 'Not now' button for Save Info pop-up upon logging in
        self._NOTIF_BUTTON = '/html/body/div[4]/div/div/div/div[3]/button[2]' # 'Not now' button for Notications pop-up upon logging in


    def _initialize_constants(self) -> None:
        '''Initializes class constants'''

        self._BASE_URL = 'https://www.instagram.com/' 
        self._TAG_URL = 'https://www.instagram.com/explore/tags/'
        self._LOGIN_URL = 'https://www.instagram.com/accounts/login/' 

        self.CHROMEDRIVER_PATH = '/assets/dependencies/chromedriver'


    def __init__(self, user: str, password: str, root_path: str) -> None:
        '''Initalizes class attributes'''

        '''
            user: username credential
            password: password credential
            root_path: root path of the instjawn program
        '''

        #Login Credentials
        self.user = user 
        self.password = password 

        self.num_posts_liked = 0 # Number of posts liked in a session

        #Initialize class constants
        self._initialize_paths()
        self._initialize_constants()

        self.root_path = root_path
        self.driver = webdriver.Chrome(self.root_path + '/assets/dependencies/chromedriver') # Automated Google Chrome browser

        self.session_num = 1 # Session number Instajawn is on

        self.logged_in = False # False = Not logged in, True = Logged in
        self.login() 
        
    '-------------------------------------------------------------------------------------------------------------------------'
    # Login Actions
    
    def click_notifications(self, load_time: int = 5) -> None:
        '''Clicks the "Not now" button for the notification pop-up'''

        '''
            load_time: Amount of time to wait for the page to load. You may have to raise this number if you have a slow connection
        '''

        self.logged_in  = True # Changes the login status to True

        self.driver.find_element_by_xpath(self._SAVE_INFO_BUTTON).click() # Dismisses Save Info pop-up

        sleep(load_time) # Waits for page to load
        
        # self.driver.find_element_by_xpath(self._NOTIF_BUTTON).click() # Dismisses Notification pop-up
        

    def login(self, load_time: int = 5) -> None:
        '''Logs into an Instagam Account based off the inputted credentials'''

        '''
            load_time: Amount of time to wait for the page to load. You may have to raise this number if you have a slow connection
        '''

        self.driver.get(self._LOGIN_URL) # Loads the login page of Instagam

        sleep(load_time) # Waits for the page to load

        # Inputs login credentials
        self.driver.find_element_by_name('username').send_keys(self.user) # Inputs the username 
        self.driver.find_element_by_name('password').send_keys(self.password) # Inputs the pasword

        self.driver.find_element_by_xpath(self._LOGIN_BUTTON).click() # Clicks the login button

        sleep(load_time) # Waits for the page to load

        self.click_notifications() # If a notifiction button pops up, program dismisses it

        sleep(load_time) # Waits for the page to load

    '-------------------------------------------------------------------------------------------------------------------------'
    # Navigating to certain pages on Instagram

    def nav_hashtag(self, hashtag: str) -> None:
        '''Loads a page by a given hashtag'''

        '''
            hashtag: a single hashtag to search
        '''

        self.driver.get(self._TAG_URL + hashtag) 


    def nav_discover(self) -> None:
        '''Naviagtes to the discover/explore page'''

        self.driver.get(self._BASE_URL + 'explore') 
    

    def nav_home_screen(self) -> None:
        '''Navigates to the home page'''

        self.driver.get(self._BASE_URL) 
    
    '-------------------------------------------------------------------------------------------------------------------------'
    # Actions to perform

    def find_xpath_button(self, button_text: str) -> list:
        '''Find the specified button based off of given XPATH text and returns it as a ClassList'''

        '''
            button_text: HTML identifier for the button in XPATH form
        '''

        return self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text)) 


    def follow_user(self) -> bool:
        '''Clicks the follow button on a users profile. Returns True if user is successfully followed, else False'''

        follow_buttons = self.find_xpath_button('Follow') 

        if follow_buttons: # Checking to see if we are not following the user
            for button in follow_buttons:  
                button.click() # Follow the user

            return True 

        else:
            return False
    

    def unfollow_user(self) -> bool:
        '''Clicks the unfollow button on a user profile. Returns True if the user is succesffully unfollowed, else False'''

        unfollow_buttons = self.find_xpath_button('Following') 

        if unfollow_buttons: # Checking to see we are following the user
            for button in unfollow_buttons:
                button.click() # Unfollow the user
                self.find_xpath_button('Unfollow')[0].click() #Finds and clicks the unfollow confirmation

            return True

        else:
            return False

    
    def like_post(self, percent_like: int = randint(90,95)) -> None:
        'Likes an Instagram Post a certain percent of the time'

        '''
            percent_like: percent chance to like the post
        '''

        if randint(1, 100) in range(percent_like): 
            self.driver.find_element_by_xpath("//*[@aria-label='{}']".format('Like')).click() 

            self.num_posts_liked +=1

    '-------------------------------------------------------------------------------------------------------------------------'

    # Storing data

    def store_num_likes(self, session_type: str):
        '''Creates and writes a new file that stores the number of likes performed in the session'''

        '''
            session_type: type of session being stored
        '''

        save_path = 'data/like_tracker/'
        current_time = str(datetime.datetime.now())
        
        file_name = current_time + '_' + session_type + '.txt'

        like_file = open(save_path + file_name, 'x') # Creates a .txt file in the like_tracker folder with the current time
        like_file.write('Session Number {}: '.format(self.session_num) + str(self.num_posts_liked)) # Wrties the number of likes performed in the session

        print('Session {} completed!'.format(self.session_num)) 
        self.session_num += 1 # Proceeds to the next session

        like_file.close()
