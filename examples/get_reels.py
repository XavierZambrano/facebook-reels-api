from facebook_uploader.uploader import FacebookReelsAPI

page_id = 'your_page_id'
page_access_token = 'your_page_access_token'

reels_api = FacebookReelsAPI(page_id, page_access_token)
reels = reels_api.get_reels(since='2020-10-31', until='2020-11-31')
