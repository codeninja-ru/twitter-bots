#!/usr/bin/env python
# coding=utf-8

import tweepy
from getpass import getpass
import ConfigParser

class PogodkaWatcherListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            #print '\n %s %s via %s\n' % (status.author.screen_name, status.created_at, status.source)
			text = status.text
			if len(text) < 100 and not text.count('@') and not text.count('http'):
				msg = status.text + " RT @" + status.author.screen_name
				self.twitter.update_status(msg)
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'
	
	
class MyTwitter(object):
	def __init__(self):
		config = ConfigParser.RawConfigParser()
		config.read('pogodka.cfg')
		self.username = config.get('twitter', 'username')
		self.password = config.get('twitter', 'password')
		self.consumer_key = config.get('twitter', 'consumer_key')
		self.consumer_secret = config.get('twitter', 'consumer_secret')
		self.consumer_key = config.get('twitter', 'consumer_key')
		self.oauth_token = config.get('twitter', 'oauth_token')
		self.oauth_secret = config.get('twitter', 'oauth_secret')

		# auth
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.oauth_token, self.oauth_secret)

		self.api = tweepy.API(self.auth)
		#api.update_status('хоршая погода')
	def update_status(self, status):
		print status
		if len(status) < 140: 
			self.api.update_status(status)

def main():
	# reading config file

#	config = ConfigParser.RawConfigParser()
#	config.read('pogodka.cfg')
#	username = config.get('twitter', 'username')
#	password = config.get('twitter', 'password')
#	consumer_key = config.get('twitter', 'consumer_key')
#	consumer_secret = config.get('twitter', 'consumer_secret')
#	consumer_key = config.get('twitter', 'consumer_key')
#	oauth_token = config.get('twitter', 'oauth_token')
#	oauth_secret = config.get('twitter', 'oauth_secret')
#
#
#	# auth
#	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#	auth.set_access_token(oauth_token, oauth_secret)
#
#	api = tweepy.API(auth)
#	#api.update_status('хоршая погода')
#

	#username = raw_input('Twitter username: ')
	#password = getpass('Twitter password: ')


	twitter = MyTwitter()
	streamListener = PogodkaWatcherListener()
	streamListener.twitter = twitter
	stream = tweepy.Stream(twitter.username, twitter.password, streamListener, timeout=None)
	stream.filter(None, ["погодка", "погода"])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
