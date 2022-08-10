# Goes through hashtags and performs actions


from random import shuffle, randint, sample
from time import sleep
from pathlib import Path
import requests
import json
import os


# Constants

'''Button Full XPATHs'''
_STORY_BUTTON = '/html/body/div[1]/section/main/header/div[1]' # Hashtag story sequence button
_FIRST_POST_BUTTON = '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div'  # First picture within the hastag sequence


'''Links'''
_SMART_TAGS_LINK = 'https://apidisplaypurposes.com/tag/' # API to fetch smart hashtags


'''Limits'''
NUM_TAGS = randint(9,15) # Number of regular hashtags to go through
NUM_SMART_TAGS = 3 # Number of smart tags to generate per given hashtag
NUM_POSTS = randint(101, 201) # Number of posts to go through

'-------------------------------------------------------------------------------------------------------------------------'
# Hashtag Initialization 

def shuffle_hashtags(hashtags_list: list, num_hashtags: int=NUM_TAGS) -> list:
    '''Shuffles the hashtag list and returns a list of random hashtags with length num_hashtags'''

    '''
        hashtags_list: list of hashtags to go through
        num_hashtags: equivalent to the length of the hashtag list
    '''

    shuffle(hashtags_list)
    return hashtags_list[:num_hashtags] # Returns the first num_hashtags of the list


def set_hashtags(file_name: str, root_path: Path) -> list: 
    '''Sets the hashtags based off the given .txt file and returns them as a list'''

    '''
        file_name: hashtag file name
        root_path: root path of the instajawn program
    '''

    file_path = Path( root_path, 'assets/hashtags/', file_name )

    # Converting hashtags into list form
    with( open( file_path ) ) as hashtag_file:
        hashtags_list = hashtag_file.read().split(',') 

    return hashtags_list


def set_smart_hashtags(hashtags_list: list, smart_tag_limit: int=NUM_SMART_TAGS) -> list:
    '''Generates and returns smart hashtags based on https://displaypurposes.com/ ranking, banned and spammy tags are filtered out'''

    '''
        hashtags_list: list of hashtags to go through
        tag_limit: number of hashtags to go through
        smart_tag_limit: number of smart tags generated per given hashtag
    ''' 

    smart_hashtags = []
    
    print('Generating smart hashtags...')

    num_tags = int(len(hashtags_list)/smart_tag_limit) # Number of smart tags generated correspond to number of regular hashtags to go through

    for tag in hashtags_list[:num_tags]:
        try: # When the website is working
            req = requests.get(_SMART_TAGS_LINK + tag)
            data = json.loads(req.text) # Get tag data

        except: # When the website is down
            print('The website appears to be down :-(')
            return # List of smart hashtags will be empty

        if data['tagExists'] is True: # If similar tags exist
            rand_num = randint(1,2) 

            if rand_num == 1: # Get highest ranked similar hashtags
                ordered_tags_by_rank = sorted(data["results"], key=lambda d: d['rank'], reverse=True) 

                for t in ordered_tags_by_rank[:smart_tag_limit]:
                    smart_hashtags.append(t['tag']) # Add smart hashtag to the list
                    print('[smart hashtag generated for <' + tag + '>: {}'.format(t)) 

            elif rand_num == 2: # Get random similar hashtags
                if len(data['results']) < smart_tag_limit: # Not enough hashtags generated
                    random_tags = sample(data['results'], len(data['results']))

                else:
                    random_tags = sample(data['results'], smart_tag_limit)

                for t in random_tags[:smart_tag_limit]:
                    smart_hashtags.append(t['tag']) # Add smart hashtag to the list
                    print('[smart hashtag generated for <' + tag + '>: {}'.format(t)) 

        else:
            print("Too few results for #{} tag".format(tag))
    
    print('-' * 50)

    return list(set(smart_hashtags))  # Delete duplicated tags by calling set()

'-------------------------------------------------------------------------------------------------------------------------'
# Actions to take on the hashtag page

def click_story(session: 'InstaJawn') -> None:
    '''Clicks and iniates the story seqeuence of the Hashtag page'''

    '''
        session: current InstaJawn selenium chrome browser session
    '''

    session.driver.find_element_by_xpath(_STORY_BUTTON).click() 


def click_next_story(session: 'InstaJawn') -> None:
    '''Clicks the next story button to progress through hashtag stories'''

    '''
        session: current InstaJawn selenium chrome browser session
    '''

    next_button = session.driver.find_element_by_class_name('coreSpriteRightChevron')
    next_button.click()


def click_first_post(session: 'InstaJawn') -> None:
    '''Clicks the first post within the hashtag sequence'''

    '''
        session: current InstaJawn selenium chrome browser session
    '''

    session.driver.find_element_by_xpath(_FIRST_POST_BUTTON).click()


def click_next_post(session: 'InstaJawn') -> None:
    '''Clicks the next button and progresses to the next post within the hashtag list'''

    '''
        session: current InstaJawn selenium chrome browser session
    '''

    session.driver.find_element_by_link_text('Next').click() 

'-------------------------------------------------------------------------------------------------------------------------'
# Sequences on the hashtag page

def view_stories(session: 'InstaJawn', wait_time: int = randint(2,4)) -> None:
    '''Views the stories for a given hashtag'''

    '''
        session: current InstaJawn selenium chrome browser session
        wait_time: amount of time to wait before moving on to the next story
    '''

    view_story = False # status of whether the hashtag has stories
    num_stories = 0 # number of stories viewed

    click_story(session=session)  # Initiates stories sequence
    
    sleep(wait_time) # Waits for the story to load

    # when there are stories for the hashtag
    if 'stories' in session.driver.current_url:
        view_story = True 

    while 'stories' in session.driver.current_url:
        click_next_story(session=session)
        sleep(wait_time)

    if view_story == True:
        print('Stories Viewed:{}\n'.format(num_stories))
    else:
        print('No stories available for this hashtag\n')

    sleep(wait_time) # Waits for the hashtag page to load 


def go_through_tags(insta_session: 'InstaJawn', hashtag_file_name: str, num_tags: int=NUM_TAGS, num_posts: int=NUM_POSTS, wait_time: int = randint(4,10)) -> None:
    '''Goes through hashtag list and performs actions'''

    '''
        insta_session: current InstaJawn selenium chrome browser session
        hashtag_file_name: name of the hashtags .txt file containing the hashtags to go through
        num_tags: number of hashtags to go through
        num_posts: total number of posts to go through for the hashtags sequence
        wait_time: amount of time to wait before moving on to the next post
    '''

    # Setting hashtag lists
    hashtags_list = set_hashtags( file_name=hashtag_file_name, root_path=insta_session.root_path )
    reduced_hashtags_list = shuffle_hashtags( hashtags_list=hashtags_list, num_hashtags=num_tags )

    # smart_hashtags = set_smart_hashtags( hashtags_list=reduced_hashtags_list )
    
    # Establishes which set of tags to use
    # tags = smart_hashtags if randint(1,2) == 1 and smart_hashtags != [] else reduced_hashtags_list
    tags = reduced_hashtags_list

    print('[{}] Running through tags:'.format( insta_session.get_time() ))

    # Printing the tags were about to run through
    for item in tags:
        print(item)
    print('-' * 50)


    like_tracker = 0

    for hashtag in tags: 
        insta_session.nav_hashtag(hashtag) # Loads the hashtag page

        print('[{}] Current tag: {}'.format( insta_session.get_time(), hashtag )) # Printing current hashtag

        sleep(wait_time) # Waits for the page to load

        view_stories(session=insta_session) # Watches the stories for the hashtag

        click_first_post(session=insta_session) # Clicks the first post on the hashtag list

        sleep(wait_time) # Waits for the first post to load
        
        try: 
            print('[{}] Beginning to like hashtag posts...\n'.format( insta_session.get_time() )) # logs
            

            for i in range(num_posts): 
                insta_session.like_post() # Like the post (maybe)

                click_next_post(session=insta_session) # Go to the next picture

                like_tracker += 1 # increment number of likes for the specific hashtag

                sleep(wait_time) # Wait for the next post to load

        except: # When a hashtag stops refreshing posts (it may happen sometimes)
            print('Hashtags stopped refreshing...moving on to the next hashtag\n') # logs
            continue # Move onto the next hashtag

        finally:
            #logs
            print('[{}] Posts liked: {} for #<{}>\n'.format( insta_session.get_time(), str(like_tracker), hashtag ) )
            print('{} total hashtag likes so far'.format(insta_session.num_posts_liked))
            print('-' * 50)

            like_tracker = 0 # resetting the like tracker for the next hashtag

    
    # insta_session.store_num_likes('HASHTAG') # Stores number of likes performed in the session
    insta_session.num_posts_liked = 0
    insta_session.nav_home_screen() # Goes back to the home screen