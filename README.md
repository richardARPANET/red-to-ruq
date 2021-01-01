# red-to-ruq

When executed this script will re-post 'hot' posts from a target Reddit.com subreddit and post that content to a destination Ruqqus.com Guild.

If ran multiple times, it will NOT repost duplicate content.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Set the following enviroment variables:

```
REDDIT_CLIENT_SECRET
REDDIT_CLIENT_ID
REDDIT_SOURCE_SUBREDDIT

RUQQUS_APP_ID
RUQQUS_APP_SECRET
RUQQUS_APP_REFRESH_TOKEN
RUQQUS_DESTINATION_GUILD
```

```bash
python red_to_ruq.py
```

Example output:

```
Skipping existing: https://youtu.be/xxxxx
Skipping existing: https://youtu.be/yyyyy
Submitting to Ruqqus: "<post_title_here>"
Skipping existing: https://streamable.com/xxxx
Submitting to Ruqqus: "<post_title_here>"
Skipping existing: https://www.youtube.com/watch?v=zzzz
Submitting to Ruqqus: "<post_title_here>"
```

See below links for information on sourcing values for these:

- https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
- https://ruqqus.com/help/oauth
