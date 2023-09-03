import pandas as pd
from facebook_uploader.uploader import FacebookReelsAPI
from facebook_uploader.reel import Reel


page_id = 'your_page_id'
page_access_token = 'your_page_access_token'
# check https://github.com/XavierZambrano/facebook-reels-api/assets/reels_to_upload.csv for a csv example
csv_path = 'your_csv_path.csv'


reels_api = FacebookReelsAPI(page_id, page_access_token)
reels_to_upload = pd.read_csv(
    csv_path, sep=',', encoding='utf-8', keep_default_na=False)

videos_uploaded = 0
videos_with_error = 0
for index, row in reels_to_upload.iterrows():
    if row['status'] == 'Uploaded':
        continue

    try:
        reel = Reel(
            description=row['description'],
            file_path=row['file_path']
        )
        reels_api.upload(reel, row['publish_time'])
    except Exception as e:
        row['status'] = f'Error {e}, fix and try again'
        videos_with_error += 1
    else:
        row['status'] = 'Uploaded'
        videos_uploaded += 1

reels_to_upload.to_csv(csv_path, sep=',', encoding='utf-8', index=False)
print('Done')
print(f'Videos uploaded: {videos_uploaded}')
print(f'Videos with error: {videos_with_error}')
print(f'For more details, check the file {csv_path}')
