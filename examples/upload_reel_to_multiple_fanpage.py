from facebook_uploader.uploader import FacebookReelsUploader
import os


pages = {
    'Name1':
        {'id': '111',
         'access_token': ''
         },
    'Name2':
        {'id': '111',
         'access_token': ''},
    'Name3':
        {'id': '111',
         'access_token': ''},
}


reels_data = {
    'file_size': 0,
    'file_path': '../assets/test_vid.mp4',
    'title': 'this is the title',
    'description': 'this is the description',
    'tags': ['frases'],
}
reels_data['file_size'] = os.path.getsize(reels_data['file_path'])
