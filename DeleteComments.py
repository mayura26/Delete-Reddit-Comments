import time
import praw

from dotenv import load_dotenv
import os
from datetime import datetime, timezone

# Load environment variables from .env file
load_dotenv('.env')

# Get the values from environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = 'script:comment_deleter:v1.0'
username = os.getenv('RUSERNAME')
password = os.getenv('PASSWORD')

# Add the subreddits you want to whitelist
whitelist = ['TheFinancialExpanse','thetagang', 'investing', 'options', 'stocks', 'FantasyPL']  
max_age = 365  # Maximum age of the comments in days
override_whitelist_with_age = True  # Set to True to override the whitelist with the maximum age
batch_size = 20
auto_confirm = True  # Set to True to automatically confirm the deletion of comments

# Connect to the Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)
reddit.validate_on_submit = True

# Check the reddit.user.me() object
if not(hasattr(reddit.user.me(), 'comments')):
    print('No comments found (or your configuration is incorrect)')
    print('Exiting...')
    exit()

# Get the user's comments
comments = list(reddit.user.me().comments.new(limit=None))
comments_to_delete = []

# Reverse the list to start with the oldest comment
comments.reverse()

# Create a set to store the subreddit names
subreddits = set()

# Generate the list of subreddits
for comment in comments:
    # Add the subreddit name to the set
    subreddits.add(comment.subreddit.display_name)

    if override_whitelist_with_age:
        # Calculate the age of the comment in days
        age = (datetime.now(timezone.utc) - datetime.fromtimestamp(comment.created_utc, timezone.utc)).days
        if age > max_age:
            comments_to_delete.append(comment)
    else:
        if comment.subreddit.display_name not in whitelist:
            comments_to_delete.append(comment)

# Print the list of subreddits
print('Subreddits:', subreddits)
print('Comments to delete:', len(comments_to_delete))

delete_choice = input('Do you wish to carry on? (y/n): ')
if delete_choice.lower() == 'n':
    print('Exiting...')
    exit()

# Group comments in sets of [batch]
if len(comments_to_delete) % batch_size == 0:
    num_groups = len(comments_to_delete) // batch_size
else:
    num_groups = len(comments_to_delete) // batch_size + 1

for i in range(num_groups):
    group_comments = comments_to_delete[i*batch_size:(i+1)*batch_size]
    print('\n************************************')
    print(f'Group {i+1}:')
    print('************************************')
    for comment in group_comments:
        # Calculate the age of the comment in days
        age = (datetime.now(timezone.utc) - datetime.fromtimestamp(comment.created_utc, timezone.utc)).days

        print(f'Subreddit: {comment.subreddit.display_name}\nComment: {comment.body}\nAge: {age} days')
    if not(auto_confirm):
        delete_choice = input('Delete these comments? (y [enter=yes]/n): ')
        
    if delete_choice.lower() == 'y' or delete_choice == '' or auto_confirm:
        for comment in group_comments:
            comment.edit('Comment deleted by user request')
            time.sleep(0.5) 
            print('Comment edited...')
            comment.delete()
            time.sleep(0.5) # Add a delay of 1 second to handle rate limits
            print('Comment deleted...')
        print('Comments deleted.')
    else:
        for comment in group_comments:
            print(f'Subreddit: {comment.subreddit.display_name}\nComment: {comment.body}\nAge: {age} days')
            delete_choice = input(f'Delete this comment? (y [enter=yes]/n): ')
            if delete_choice.lower() == 'y' or delete_choice == '':
                comment.edit('Comment deleted by user request')
                time.sleep(0.5) 
                comment.delete()
                time.sleep(0.5) 
                print('Comment deleted.')
            else:
                print('Comment not deleted.')