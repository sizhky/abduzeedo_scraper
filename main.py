import logging
import os.path
import sys
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.DEBUG)
logger.info("running %s" % ' '.join(sys.argv))


import urllib2
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

class RSS_Checker(object):
	"""Checks for new links from abdz and returns new 
	items based on search time"""
	def __init__(self, config_file = 'config.txt'):
		self.config_file = config_file
		self.feed_link = 'http://abduzeedo.com/rss.xml'
		time_format = '%a, %d %b %Y %H:%M:%S'
		with open(config_file, 'r') as f:
			time = f.read()
			self.last_checked = datetime.strptime(time, time_format)
			logger.info('RSS links last checked {} ago'.format(datetime.now() - self.last_checked))

		with open(config_file, 'w') as f:
			f.write(datetime.strftime(datetime.now(), time_format))
		self.items = []
		self.process()

	def process(self):
		page = urllib2.urlopen(self.feed_link)
		soup = BeautifulSoup(page, 'lxml')
		x = str(soup)
		x = x.replace('&lt;', '<').replace('&gt;', '>')
		soup = BeautifulSoup(x, 'lxml')
		items = str(soup).split('<item>')
		self.pages = soup.find_all('item')
		for page in self.pages:
			item = self.get_attrs(page)
			if item['time'] > self.last_checked:
				self.items.append(item)

	def get_attrs(self, page):
		regexp = r'http.*(?=\n)'
		link = str(page).split('<link/>')
		
		link = re.search(regexp, link[1]).group()
		try:
			time = page.find('pubdate').getText()[:-6]
			time = datetime.strptime(time, '%a, %d %b %Y %H:%M:%S')
		except Exception as e:
			print(e)
			time = -1
		imgs = map(lambda x: x.get('src'), page.find_all('img'))
		item = {'url': link, 'time': time, 'imgs': imgs}
		logger.debug('scraping {}'.format(item['url']))
		return(item)
				

class imgur_uploader(object):
	"""uploads images to imgur from a list of URLs, 
	creates an album and uploads it onto reddit"""
	def __init__(self, item, reddit, subreddit, imgur_client):
		self.item = item
		self.reddit = reddit
		self.subreddit = subreddit
		self.imgur_client = imgur_client
		album_id = self.upload()
		submitted_link = self.submit_link(self.subreddit, self.album_title, url = 'http://imgur.com/a/'+album_id)
		logger.info("Submission successful! Find it @ reddit.com/r/feedtesting/{}".format(submitted_link))

	def upload(self):
		self.album_title = self.item['url'].split('/')[-1]
		album = imgur_client.create_album(fields = {'title': self.album_title})
		album_id = album['id']
		logger.info('Started uploading @ {}'.format(album_id))
		for i, file_ in enumerate(self.item['imgs']):
			logger.debug('Uploading {}'.format(file_))
			self.upload_image(self.imgur_client, file_, config = {'album':album_id, 'title':str(i)})
		logger.info('uploaded images to imgur.com/a/{}'.format(album_id))
		return(album_id)

	def upload_image(self, client, file_, config):
		try:
			client.upload_from_url(file_, config = config, anon = 0)
			return(None)
		except Exception as e:
			logger.info(str(e))
			logger.info('imgur upload timed out... Retrying in 60s')
			time.sleep(60)        
			return(self.upload_image(client, file_, config))

	def submit_link(self, subreddit, link_title, url):
		try:
				submitted_link = subreddit.submit(link_title, url = url)
				return(submitted_link)
		except Exception as e:
				logger.info('subreddit upload timed out... Retrying in 60s')
				logger.info(str(e))
				time.sleep(60)
				return(self.submit_link(subreddit, link_title, url))

if __name__ == '__main__':
	from clients import get_clients
	(reddit, subreddit, imgur_client) = get_clients()
	rss_checker = RSS_Checker(config_file = 'config.txt')
	for item in rss_checker.items:
		logger.info('uploading album '+item['url'])
		imgur_uploader(item, reddit, subreddit, imgur_client)

