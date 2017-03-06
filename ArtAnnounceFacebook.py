import os  # To access our OS environment variables
import facebook 
# "pip install facebook" into an active virtual env

# Using Python os.environ to get environmental variables

# Note: you must run `source secrets.sh` before running 
# this file to set required environmental variables.

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph

cfg = {
"page_id"      : os.environ["FB_CLIENT_ID"],  # fb page ID
"access_token" : os.environ["FB_EXCHANGE_TOKEN"]   # fb access token
}

api = get_api(cfg)

def post_to_fb(fb_post, img_url):
#msg = "Second post!"
#status = api.put_wall_post(msg)
#status = api.put_photo(image=open("https://fasoimages-4cde.kxcdn.com/25287_1432515l+v=201609181617c201609181617error/accepting-is.jpg"))
#import pdb; pdb.set_trace()
#status = api.put_wall_post(photo="https://fasoimages-4cde.kxcdn.com/25287_1432515l+v=201609181617c201609181617error/accepting-is.jpg")

	status = api.put_wall_post(fb_post, {
	     'name': '',
	     'link': img_url,
	     'caption': '',
	     'description': '',
	     'picture': img_url
	})

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

# if __name__ == "__main__":
#   main()