import re
import tweepy
import datetime
from tweepy import OAuthHandler
from textblob import TextBlob
from django.conf import settings

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		self.consumer_key = settings.API_KEY
		self.consumer_secret = settings.API_KEY_SECRET
		self.access_token = settings.ACCESS_TOKEN
		self.access_token_secret = settings.ACCESS_TOKEN_SECRET
		self.bearer_key = settings.BEARER_TOKEN
		# attempt authentication
		try:
			# create Client 
			self.client = tweepy.Client(bearer_token=settings.BEARER_TOKEN,
										consumer_key=settings.API_KEY,
                                   		consumer_secret=settings.API_KEY_SECRET,
                                   		access_token=settings.ACCESS_TOKEN,
                                   		access_token_secret=settings.ACCESS_TOKEN_SECRET)
			# set access token and secret
			
		except tweepy.errors.TweepyException as e:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'Positive'
		elif analysis.sentiment.polarity == 0:
			return 'Neutral'
		else:
			return 'Negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.client.search_recent_tweets(query = query, tweet_fields=['created_at','public_metrics','possibly_sensitive'], expansions=['author_id'], max_results = count)

			# parsing tweets one by one
			count = 0
			for tweet in fetched_tweets.data:
				count+=1
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}
				# saving text of tweet
				parsed_tweet['id'] = count
				parsed_tweet['text'] = tweet.text
				# saving author  of tweet
				parsed_tweet['author'] = tweet.author_id
				# saving tweet creation date
				parsed_tweet['date'] = tweet.created_at
				#saving retweet count of tweet
				parsed_tweet['retweet_count'] = tweet.public_metrics['retweet_count']
				# saving user details
				users = self.client.get_users(ids=tweet.author_id, user_fields=['profile_image_url','public_metrics','created_at'])
				
				for user in users.data:
					# print(user.profile_image_url)
					# print(user.username)
					url = ' '.join(re.sub("_normal", "", user.profile_image_url).split())
					parsed_tweet['profile_url'] = url
					parsed_tweet['username'] = user.username
					parsed_tweet['name'] = user.name
					parsed_tweet['followers_count'] = user.public_metrics["followers_count"]
					parsed_tweet['following_count'] = user.public_metrics["following_count"]
					following = user.public_metrics["following_count"]
					followers = user.public_metrics["followers_count"]
					# Bot
					created_at = user.created_at
					
					today = datetime.datetime.now(tz=datetime.timezone.utc)
				
					days_before = (today-datetime.timedelta(days=15))

					#usertweets
					user_tweets = self.client.get_users_tweets(id=user.id, tweet_fields=['created_at','public_metrics'],expansions=['author_id'], max_results=100)
					userTweetsLength = len(user_tweets)
					# print(len(user_tweets.data),'tweets_count')
					if created_at >= days_before and userTweetsLength >= 15:
						parsed_tweet['fbot'] = 'Yes'
					else:
						parsed_tweet['fbot'] = 'No'
					# if following >= 100 and followers < 50:
					# 	parsed_tweet['fbot'] = 'Yes'
					# else:
					# 	parsed_tweet['fbot'] = 'No'
				parsed_tweet['sensitive'] = tweet.possibly_sensitive
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				# if tweet.retweet_count > 0:
				# 	# if tweet has retweets, ensure that it is appended only once
				# 	if parsed_tweet not in tweets:
				# 		tweets.append(parsed_tweet)
				# else:
				tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.errors.TweepyException as e:
			# print error (if any)
			print("Error : " + str(e))

	def get_user(self, usernames):

		user_data=[]
		try:
			users = self.client.get_users(usernames=usernames, user_fields=['profile_image_url','url','description','public_metrics'])

			for user in users.data:
				parsed_user={}
				
				url = ' '.join(re.sub("_normal", "", user.profile_image_url).split())

				#saving username
				parsed_user['username'] = user.username
				#saving profile url
				parsed_user['profile_url'] = url

				parsed_user['name'] = user.name

				parsed_user['id'] = user.id
				if user.url:
					parsed_user['url'] = user.url
				if user.description:
					parsed_user['description'] = user.description
				parsed_user['followers_count'] = user.public_metrics["followers_count"]
				parsed_user['following_count'] = user.public_metrics["following_count"]

				

				user_data.append(parsed_user)
			return user_data
				

		except tweepy.errors.TweepyException as e:
			# print error (if any)
			print("Error : " + str(e))

	def get_user_tweets(self, id):

		tweets_data=[]
		try:
			tweets = self.client.get_users_tweets(id=id, tweet_fields=['created_at','public_metrics'],expansions=['author_id'], max_results=10)

			for tweet in tweets.data:
				parsed_data={}
				parsed_data['text'] = tweet.text
				
				
				parsed_data['date'] = tweet.created_at
				# saving user details
				users = self.client.get_users(ids=tweet.author_id, user_fields=['profile_image_url'])
				#saving retweet count of tweet
				parsed_data['retweet_count'] = tweet.public_metrics['retweet_count']
				


				for user in users.data:
					# print(user.profile_image_url)
					# print(user.username)
					url = ' '.join(re.sub("_normal", "", user.profile_image_url).split())
					parsed_data['profile_url'] = url
					parsed_data['username'] = user.username
					parsed_data['name'] = user.name

					# saving sentiment of tweet
					parsed_data['sentiment'] = self.get_tweet_sentiment(tweet.text)

					# appending parsed tweet to tweets list
					# if tweet.retweet_count > 0:
					# 	# if tweet has retweets, ensure that it is appended only once
					# 	if parsed_tweet not in tweets:
					# 		tweets.append(parsed_tweet)
					# else:
			
				tweets_data.append(parsed_data)
			return tweets_data
				

		except tweepy.errors.TweepyException as e:
			# print error (if any)
			print("Error : " + str(e))

# class TwitterClientV1(object):
		def __init__(self):
		
			# keys and tokens from the Twitter Dev Console
			self.consumer_key = settings.API_KEY
			self.consumer_secret = settings.API_KEY_SECRET
			self.access_token = settings.ACCESS_TOKEN
			self.access_token_secret = settings.ACCESS_TOKEN_SECRET
			self.bearer_key = settings.BEARER_TOKEN
			# attempt authentication
			try:
				# create Client 
				auth = tweepy.OAuth1UserHandler(consumer_key=settings.API_KEY,
												consumer_secret=settings.API_KEY_SECRET,
												access_token=settings.ACCESS_TOKEN,
												access_token_secret=settings.ACCESS_TOKEN_SECRET)

				self.client = tweepy.API(auth)
				
				# set access token and secret
				
			except tweepy.errors.TweepyException as e:
				print("Error: Authentication Failed")

		def get_trends(self):
			trends=[]
			try:
				tags = self.client.get_place_trends(23424848)
				count=0
				
				for tag in tags[0]["trends"]:
					if count<10:
						count+=1
						# print(tag["name"])
						trends.append(tag)
				return trends
			
			except tweepy.errors.TweepyException as e:
				# print error (if any)
				print("Trends_Error : " + str(e))