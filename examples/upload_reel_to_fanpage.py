from facebook_uploader.uploader import FacebookReelsAPI
from facebook_uploader.reel import Reel


page_id = 'your_page_id'
page_access_token = 'your_page_access_token'

# timestamps and yyyy-mm-dd hh:mm:ss in UTC
# if publish_time is None, the reel will be published immediately
publish_time = None
file_path = '../assets/test_vid_00.mp4'
description = 'The reels description #hashtag1 #hashtag2 #hashtag3'


reels_api = FacebookReelsAPI(page_id, page_access_token)
reel = Reel(description=description, file_path=file_path)
reels_api.upload(reel, publish_time)
