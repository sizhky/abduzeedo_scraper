from imgurpython import ImgurClient
# import image_collector
import os
import praw

import logging
import os.path
import sys
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

URL = 'http://abduzeedo.com/daily-design-inspiration-178'

def get_clients():
  CLIENT_ID = 'f6b55c4c63de8411'
  CLIENT_SECRET = '5c2e28b4d73fd5599bf4c394d0165d45dfdae0a52'
  ACCESS_TOKEN = 'bad0ee1b8356d91d961e1e89690e11f16f1156083'
  REFRESH_TOKEN = '9f5dfc928b1fe5b9a51ee46f4db21b41bae886614'

  ##auth_url = client.get_auth_url('pin')
  ##
  ##credentials = client.authorize('7fd0bb2377', 'pin')
  ##client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
  ##print('access token: {}\nrefresh_token: {}'.format(credentials['access_token'], credentials['refresh_token']))


  imgur_client = ImgurClient(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)
  imgur_client.set_user_auth(ACCESS_TOKEN, REFRESH_TOKEN)

  reddit = praw.Reddit(client_id='anlOIy2SKazBqZA',
                       client_secret='bajOvPWgxHIBrOMOk6GRmBI8bG4o',
                       password='coffee*2',
                       user_agent='abdulinker',
                       username='CoffeeSmoker_bot')

  subreddit = reddit.subreddit('feedtesting')
  logger.debug('Currently working from {}'.format(os.getcwd()))
  return(reddit, subreddit, imgur_client)

# def move_images(url):
#   if not os.path.isdir(url.split('/')[-1]):
#     logger.info('collecting images')
#     directory = image_collector.get_images_from_url(url)
#   else:
#     logger.info('already found the directory')
#     directory = url.split('/')[-1]
#   album_link = image_collector.upload_to_imgur(imgur_client, directory)
#   submitted_link = image_collector.submit_link(subreddit, directory, url = 'http://imgur.com/a/'+album_link)
#   logger.info("Submission successful! Find it @ reddit.com/r/feedtesting/{}".format(submitted_link))
#   return(album_link, submitted_link)

if __name__ == '__main__':
  (reddit, subreddit, imgur_client) = get_clients()
  move_images(URL)


##if(link_checker.new_link_in_rss()):
##  link_checker.get_new_links
##  for url in urls:
##    move_images(url)
