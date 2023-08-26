from facebook_uploader.uploader import FacebookReelsUploader
import os


page = {
    'page_name': 'name',
    'page_id': '1111',
    'page_access_token': ''
}
publish_time = None
reels_data = {
    'file_size': 0,
    'file_path': '../assets/test_vid (4).mp4',
    'title': 'Verdades',
    'description': 'Verdades',
    'tags': ['frases'],
}

reels_data['file_size'] = os.path.getsize(reels_data['file_path'])
uploader = FacebookReelsUploader(page['page_id'], page['page_access_token'])
uploader.upload(
    reels_data,
    publish_time=publish_time
)
