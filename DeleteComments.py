import praw

from dotenv import load_dotenv
import os
from datetime import datetime, timezone

# Load environment variables from .env file
load_dotenv('.env')

# Get the values from environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')
username = os.getenv('RUSERNAME')
password = os.getenv('PASSWORD')

# Add the subreddits you want to whitelist
whitelist = ['thetagang', 'TheFinancialExpanse', 'investing', 'options', 'Vitards', 'stocks', 'FantasyPL']  

# Connect to the Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

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
    if comment.subreddit.display_name not in whitelist:
        comments_to_delete.append(comment)

# Print the list of subreddits
print('Subreddits:', subreddits)
print('Comments to delete:', len(comments_to_delete))

delete_choice = input('Do you wish to carry on? (y/n): ')
if delete_choice.lower() == 'n':
    print('Exiting...')
    exit()

# Group comments in sets of 10
if len(comments_to_delete) % 10 == 0:
    num_groups = len(comments_to_delete) // 10
else:
    num_groups = len(comments_to_delete) // 10 + 1

for i in range(num_groups):
    group_comments = comments_to_delete[i*10:(i+1)*10]
    print(f'Group {i+1}:')
    for comment in group_comments:
        # Calculate the age of the comment in days
        age = (datetime.now(timezone.utc) - datetime.fromtimestamp(comment.created_utc, timezone.utc)).days

        print(f'Subreddit: {comment.subreddit.display_name}\nComment: {comment.body}\nAge: {age} days')
    delete_choice = input('Delete these comments? (y [enter=yes]/n): ')
    if delete_choice.lower() == 'y' or delete_choice == '':
        for comment in group_comments:
            comment.delete()
        print('Comments deleted.')
    else:
        print('Comments not deleted.')