import os
from urllib.parse import urlparse

import praw

SOURCE_SUBREDDIT = os.environ['SOURCE_SUBREDDIT']
REDDIT_SECRET = os.environ['REDDIT_SECRET']
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
RUQQUS_CODE = os.environ['RUQQUS_CODE']
SOURCE_DOMAIN_BLACKLIST = (
    'v.redd.it',
    'reddit.com',
    'www.reddit.com',
)
REDDIT = praw.Reddit(
    user_agent='my_cool_application',
    client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_SECRET
)


def get_reddit_submissions():
    submissions = REDDIT.subreddit(SOURCE_SUBREDDIT).hot(limit=50)
    for submission in submissions:
        title = submission.title
        url = submission.url
        url_data = urlparse(url)
        if url_data.netloc in SOURCE_DOMAIN_BLACKLIST:
            continue
        yield title, url


def main():
    for title, url in get_reddit_submissions():
        print(title, url)


if __name__ == '__main__':
    main()
