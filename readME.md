# ![InstaJawn Cover](/creatives/cover.png)
A starting point to Instagram automation using selenium for autonomous web actions.
  

## What InstaJawn Does so Far
So far, the main action that InstaJawn can do is like posts. It does this in 2 ways:

### Hashtags
- Read from a user inputted .txt file with hashtags in it.
- Generates similar smart hashtags based off of an external API.
- Navigates to the hashtag pages.
- Viewes stories from hashtag pages. 
- Continuously likes posts on a hashtag page.

### Feed
- Goes through a feed and likes posts

The amount of likes performed can be toggled on the top lines within feed.py and hashtag.py under the # Constants section.
Additionally, InstaJawn records the number of likes performed in one session. You can find these .txt files within the data/like_tracker folder.


## How To Run
1) Load hashtags text file into the assets/hashtags folder. See inside for a template!
2) Go into main.py within the modules folder and input the necessary information.

You're good to go! Run main.py to see InstaJawn do its thing.


## Customization
This is meant to serve as a base. It may or may not be further developed on, but there is room for a lot of customization if you choose to build a project on top of this program. Some ideas:

- Change InstaJawn variables the way you see fit. Switch up the number of posts to go through within both the hashtag & feed sequence, the wait/load time for pages to load, the percent chance to like a post.
- You might noticed a follower_tracker folder under the data folder along with methods within instajawn.py that enable the ability to follow and unfollow users. See if you can manage your followers with InstaJawn!
- If account information is not inputted before program launch, the user is prompted to enter it in the terminal. A graphical user interface can be implemented to make this a more visually appealing process.
- Deploy InstaJawn to a cloud or local server. You may have noticed a prelimary Dockerfile - play around with it!

This list is by no means exhaustive, so get creative and implement your own features if you are up for it!

## Notes
This has not been heavily tested yet - consider this beta code. I take no responsibility if your Instagram accounts get banned as a result of using this code - it is meant soley for learning purposes.
