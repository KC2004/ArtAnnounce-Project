import os  # To access our OS environment variables
#import tweepy
import twitter # Available on lab machines
# Otherwise "pip install" into an active virtual env

# Using Python os.environ to get environmental variables
#
# Note: you must run `source secrets.sh` before running 
# this file to set required environmental variables.

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# This will print info about credentials to make sure 
# they're correct
print api.VerifyCredentials()


# Send a tweet
def post_tweet(tweet_str, tweet_url):
	#status = api.PostUpdate("my second tweet in ArtShare")

	status = api.PostMedia(tweet_str, tweet_url)
	print status.text



