import csv
import datetime
from six.moves import (
    configparser,
    input,
)
import sys
import twitter


USAGE = '''Usage: python adiaux.py archive before_date

archive     - the csv file from your downloaded twitter archive
before_date - the cut-off date for tweets; tweets posted before that date will
              be deleted.

You must fill out adiaux.ini with your API keys.  See README.md for deets.
'''

if len(sys.argv) != 3:
    print(USAGE)
    sys.exit(1)

try:
    date_from = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
except:
    print("    I couldn't parse the date I was given")
    print(USAGE)
    sys.exit(2)


tweets_to_delete = []
try:
    print('Parsing your twarchive...')
    with open(sys.argv[1]) as tweet_archive:
        reader = csv.DictReader(tweet_archive)
        for row in reader:
            tweet_date = datetime.datetime.strptime(
                row['timestamp'].split(' ')[0],
                '%Y-%m-%d')
            delta = date_from.date() - tweet_date.date()
            if delta.days > 0:
                # print("before_date: {} - tweet_date: {}".format(
                #     date_from.date(), tweet_date.date()))
                tweets_to_delete.append(row['tweet_id'])
except Exception as e:
    print("    I couldn't open tweet archive file or file was malformed")
    print(e)
    print(USAGE)
    sys.exit(3)

config = configparser.ConfigParser()
config.read('adiaux.ini')

api = twitter.Api(
    consumer_key=config['adiaux']['consumer_key'],
    consumer_secret=config['adiaux']['consumer_secret'],
    access_token_key=config['adiaux']['access_token_key'],
    access_token_secret=config['adiaux']['access_token_secret'],
    sleep_on_rate_limit=True)

try:
    print('Verifying twitter creds...')
    api.VerifyCredentials()
except:
    print("    I couldn't verify your credentials; check adiaux.ini")
    print(USAGE)
    sys.exit(4)

print('Okay, this is could take a LONG time')
print('I am going to attempt to delete {} tweets, as many as I can'
      'at a time.'.format(
          len(tweets_to_delete)))
print('However, I can only do so many every *mumble* minutes and then I '
      "sleep because of twitter's rate limiting.")
print("Long time, right? I'm also going to be REALLY VERBOSE. Not sorry.")
print('Maybe run this in a screen or tmux session.')
confirm = input('Are you ready for this? [y/n]> ')
if confirm.lower()[0] != 'y':
    print('Okay, aborting')
    sys.exit(5)
confirm = input('Last chance. Are you SUPER SURE? [y/n]> ')
if confirm.lower()[0] != 'y':
    print('Okay, aborting')
    sys.exit(6)

i = 0
for tweet in tweets_to_delete:
    i += 1
    try:
        print('{}. Destroying {}'.format(i, tweet))
        api.DestroyStatus(tweet)
    except Exception as e:
        print("{}: Couldn't destroy {} - already deleted? Moving on...".format(
            e, tweet))
    if i % 25 == 0:
        print('    {} deleted...'.format(i))

print("I believe I'm done here, but you should go to twitter.com and check.")
print('Be safe out there!')
