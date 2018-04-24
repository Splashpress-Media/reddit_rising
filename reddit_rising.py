import requests 
import os
from collections import OrderedDict
from slackclient import SlackClient
import praw

reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='Reddit_Rising by /u/easy_c0mpany80')

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
	
if __name__ == '__main__':
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
