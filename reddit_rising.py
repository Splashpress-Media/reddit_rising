import requests 
import os
from collections import OrderedDict
from slackclient import SlackClient
import praw

reddit = praw.Reddit(client_id='#############',
                     client_secret='##############',
                     user_agent='Reddit_Rising by /u/easy_c0mpany80')

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

slack_client = SlackClient(SLACK_TOKEN)

def get_reddit():

	news_titles = []
	news_urls = []

	subreddit = reddit.subreddit('news')
	
	for submission in subreddit.rising(limit=3):
		
		news_titles.append(str(submission.title.encode('utf-8')))
		news_urls.append(submission.url)
		
	reddit_data = OrderedDict(zip(news_titles, news_urls))
	
	print(reddit_data)
		
	return reddit_data

def list_channels():
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
	channels = list_channels()
	
	reddit_data = get_reddit()
		
	if channels:
		print("Channels: ")
		for channel in channels:
			print(channel['name'] + ' - ' + channel['id'])	
			
			if channel['name'] == 'snd-editorial':
				if reddit_data:
					send_message(channel['id'], reddit_data)
			
	else:
		print("Unable to authenticate")