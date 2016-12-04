# adia&#365;

Say adia&#365; to your old tweets.

## Setup

1. First, you'll need to create an app and generate all of your tokens. Go to <https://apps.twitter.com> and create a new app. Fill out your details (it's a pain), leaving the callback url blank. Click on the 'Keys and Access Tokens' tab and from there generate an access token.
2. Store these tokens in `adiaux.ini` - the config entries should match up pretty well with what Twitter gives you
3. Next, download your Twitter archive by going to your settings. At the bottom of the Account page, request your Twitter archive. Unzip this and keep the `tweets.csv` file handy.

## Running

First, you'll need python and virtualenv, then you'll need to install the requirements. You can do this like so:

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Then you can run the script like so:

```
Usage: python adiaux.py archive before_date

archive     - the csv file from your downloaded twitter archive
before_date - the cut-off date for tweets; tweets posted before that date will
              be deleted.

You must fill out adiaux.ini with your API keys.  See README.md for deets.
```

It will attempt to load the tweets from the CSV file you gave it and check for tweets that were posted before the date you gave it. Next, it will attempt to connect to twitter with the credentials you gave it in the ini file. Finally, it will attempt to delete all of the tweets it found.

If all goes well, you should see something like the following:

```
$ python adiaux.py tweets.csv 2016-01-01
Parsing your twarchive...
Verifying twitter creds...
Okay, this is could take a LONG time
I am going to attempt to delete 11344 tweets, fifteen at a time.
However, I can only do fifteen every fifteen minutes and then I sleep.
Long time, right? I'm also going to be REALLY VERBOSE. Not sorry.
Maybe run this in a screen or tmux session.
Are you ready for this? [y/n]> y
Last chance. Are you SUPER SURE? [y/n]> y
1. Destroying 12345678
2. Destroying 12345679
...
Rate limited, sleeping until we can continue
16. Destroying 12345680
...
```

You'll have to confirm twice to be doubly sure. This is permanent, after all!

**Caution:** this will take forever, and it will be *very* verbose.  Twitter is heavily rate-limited for apps doing this sort of thing - It's usually set up so that you can delete fifteen tweets every fifteen minutes.  Slow, right? So I suggest running this in a `screen` or `tmux` session and going to bed or out to dinner or something.

## Rationale

Your Twitter account is *your* space to do with what *you* wish. I wrote this thing because I started getting super dysphoric about my old tweets, particularly those with pictures of me in them. I tried to go through and delete the media so that they wouldn't show up on a deep dive, but that proved to be stupidly hard. "Perhaps python will fix my dysphoria," I thought, and so I did this.

Be safe, of course, but remember, your account is *your* space, and don't let anyone tell you otherwise.
