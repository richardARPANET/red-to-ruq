import os
from urllib.parse import urlparse

import praw
from ruqqus import RuqqusClient

REDDIT_SOURCE_SUBREDDIT = os.environ['REDDIT_SOURCE_SUBREDDIT']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
try:
    REDDIT_HOT_LIMIT = int(os.environ['REDDIT_HOT_LIMIT'])
except KeyError:
    REDDIT_HOT_LIMIT = 50
SOURCE_DOMAIN_BLACKLIST = (
    'v.redd.it',
    'reddit.com',
    'www.reddit.com',
)
REDDIT = praw.Reddit(
    user_agent='my_cool_application',
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
)

RUQQUS_APP_ID = os.environ['RUQQUS_APP_ID']
RUQQUS_APP_SECRET = os.environ['RUQQUS_APP_SECRET']
RUQQUS_APP_REFRESH_TOKEN = os.environ['RUQQUS_APP_REFRESH_TOKEN']
RUQQUS_DESTINATION_GUILD = os.environ['RUQQUS_DESTINATION_GUILD']
RUQQUS_CLIENT = RuqqusClient(
    client_id=RUQQUS_APP_ID,
    client_secret=RUQQUS_APP_SECRET,
    refresh_token=RUQQUS_APP_REFRESH_TOKEN,
)


def _submit_to_ruqqus(*, title, url):
    RUQQUS_CLIENT.submit_post(
        guild=RUQQUS_DESTINATION_GUILD, url=url, title=title
    )


def _get_reddit_submissions():
    submissions = REDDIT.subreddit(REDDIT_SOURCE_SUBREDDIT).hot(
        limit=REDDIT_HOT_LIMIT
    )
    for submission in submissions:
        title = submission.title
        url = submission.url
        url_data = urlparse(url)
        if url_data.netloc in SOURCE_DOMAIN_BLACKLIST:
            continue
        yield title, url


def _get_all_post_urls_in_guild(name):
    def _get_all_guild_posts(name):
        all_posts = []
        page = 1
        while True:
            posts = RUQQUS_CLIENT.get_guild_posts(
                name='CertifiedFreakouts', page=page
            )
            all_posts.extend(posts['data'])
            if not posts['next_exists']:
                break
            page += 1
        return all_posts

    return set(p['url'] for p in _get_all_guild_posts(name=name))


def main():
    existing_ruqqus_post_urls = _get_all_post_urls_in_guild(
        name=RUQQUS_DESTINATION_GUILD
    )

    for title, url in _get_reddit_submissions():
        if url in existing_ruqqus_post_urls:
            print(f'Skipping existing: {url}')
            continue
        print(f'Submitting to Ruqqus: "{title}"')
        _submit_to_ruqqus(title=title, url=url)


if __name__ == '__main__':
    main()
