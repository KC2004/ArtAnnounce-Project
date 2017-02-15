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



# import tweepy

# auth = tweepy.OAuthHandler(consumer_key=os.environ['TWITTER_CONSUMER_KEY'], consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'])
# auth.set_access_token(access_token=os.environ['TWITTER_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
# auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN_KEY'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


# api = tweepy.API(auth)
# print os.environ['TWITTER_CONSUMER_KEY']
# This will print info about credentials to make sure 
# they're correct
print api.VerifyCredentials()

# # main
# input_path = "green-eggs.txt"

# # Open the file and turn it into one long string
# input_text = markov.open_and_read_file(input_path)

# # Get a Markov chain
# chains = markov.make_chains(input_text)

# # Produce random text
# random_text = markov.make_text(chains)

# if len(random_text) <= 144:

# Send a tweet
status = api.PostUpdate("my first tweet in ArtShare")
print status.text


# status = api.update_status("my first tweet in ArtShare")
# print status.text
# If you updated secrets.sh, you can go to your Twitter 
# timeline to see it.

