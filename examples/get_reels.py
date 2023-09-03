from facebook_uploader.uploader import FacebookReelsAPI

page_id = 'your_page_id'
page_access_token = 'your_page_access_token'

# today, yesterday, timestamps, yyyy-mm-dd (2020-10-31)
since = '2020-10-31'
until = '2020-11-31'

reels_api = FacebookReelsAPI(page_id, page_access_token)
reels = reels_api.get_reels(since=since, until=until)
