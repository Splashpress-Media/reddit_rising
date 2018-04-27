import requests 
import os
from collections import OrderedDict
from slackclient import SlackClient
import praw

#environment variables need to be setup in AWS Lambda options
PRAW_CLIENT = os.environ.get('PRAW_CLIENT')
PRAW_SECRET = os.environ.get('PRAW_SECRET')
PRAW_AGENT = os.environ.get('PRAW_AGENT')

reddit = praw.Reddit(client_id= PRAW_CLIENT,
                     client_secret= PRAW_SECRET,
                     user_agent= PRAW_AGENT)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

slack_client = SlackClient(SLACK_TOKEN)

def get_reddit():

	news_titles = []
	news_urls = []

	subreddit = reddit.subreddit('news')
	
	for submission in subreddit.rising(limit=3):
		
		news_titles.append(str(submission.title.encode('utf-8')))
		news_urls.append(submission.url.encode('utf-8'))
		
	reddit_data = OrderedDict(zip(news_titles, news_urls))
	
	
	return reddit_data
	

def get_channels():
	channels_call = slack_client.api_call("channels.list")
	if channels_call.get('ok'):
		return channels_call['channels']
	return None 
	
def send_message(channel_id, message):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=message,
		username='Reddit Rising News Bot',
		icon_emoji=':robot_face:')
	
def lambda_handler(event, context):
	print('Inside lambda_handler')
	channels = get_channels()

	reddit_data = get_reddit()

	if channels:
		for channel in channels:
			if channel['name'] == 'snd-editorial':
				if reddit_data:
					for k,v in reddit_data.items():
						send_message(channel['id'], k+v)

	else:
		print("Unable to authenticate")
