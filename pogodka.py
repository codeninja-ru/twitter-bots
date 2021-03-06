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
				self.twitter.reply(msg, status.id)
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
	def tweet(self, status):
		print status
		if len(status) < 140: 
			self.api.update_status(status)
	
	def reply(self, status, in_reply_to_status_id):
		print status
		if len(status) < 140:
			self.api.update_status(status, in_reply_to_status_id)

def main():
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
