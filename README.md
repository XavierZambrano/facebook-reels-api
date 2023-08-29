# Facebook Reels API

Python wrapper for the [Facebook Reels API](https://developers.facebook.com/docs/video-api/guides/reels-publishing)

## Documentation

- [Installation](#installation) 
- [Dependencies](#dependencies) 
- [Usage](#usage)
- [Instance Methods](#instance-methods)

## Installation
TODO

## Dependencies
- [requests](https://pypi.org/project/requests/)

## Usage

### Create an instance
```
from facebook_uploader.uploader import FacebookReelsAPI
from facebook_uploader.reel import Reel


page_id = 'your_page_id'
page_access_token = 'your_page_access_token'
reels_api = FacebookReelsAPI(page_id, page_access_token)
```

### Upload a Reel
```
from facebook_uploader.uploader import FacebookReelsAPI
from facebook_uploader.reel import Reel


page_id = 'your_page_id'
page_access_token = 'your_page_access_token'

# today, yesterday, timestamps, yyyy-mm-dd (2020-10-31)
# if publish_time is None, the reel will be published immediately
publish_time = None
file_path = 'video.mp4'
description = 'The reels description #hashtag1 #hashtag2 #hashtag3'

reels_api = FacebookReelsAPI(page_id, page_access_token)
reel = Reel(description=description, file_path=file_path)
reels_api.upload(reel, publish_time)
```

### Get Reels
```
from facebook_uploader.uploader import FacebookReelsAPI

page_id = 'your_page_id'
page_access_token = 'your_page_access_token'

reels_api = FacebookReelsAPI(page_id, page_access_token)
reels = reels_api.get_reels(since='2020-10-31', until='2020-11-31')
```

## Instance Methods
- is_page_access_token_valid
- upload
- _initialize_upload
- _process_upload
- _publish
- upload_status
- get_reels
- json (attribute, return the json response from the last request)