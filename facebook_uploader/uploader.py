import requests
from facebook_uploader.exceptions import InvalidPageAccessTokenError
# api docs https://developers.facebook.com/docs/video-api/guides/reels-publishing


class FacebookReelsUploader:
    def __init__(self, page_id, page_token):
        self.page_id = page_id
        self.page_access_token = page_token
        self.video = None

    def is_page_access_token_valid(self):
        # /video_reels is to get reels published,
        # but it works to validate the page_access_token
        # and /debug_token requires an app access token
        url = f"https://graph.facebook.com/v15.0/{self.page_id}/video_reels"
        params = {
            'since': 'today',
            'access_token': self.page_access_token
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return True
        else:
            return False

    def upload(self, video, publish_time=None):
        hashtags = ' '.join([f'#{tag}' for tag in video["tags"]])
        video_description_with_hashtags = f'{video["description"]} {hashtags}'

        video['video_id'] = None
        video['file_data'] = open(video['file_path'], 'rb')
        video['description'] = video_description_with_hashtags
        video['publish_time'] = publish_time
        self.video = video

        print(f'Initializing upload...')
        self._initialize_upload()

        print(f'Uploading...')
        self._process_upload()
        if not self._is_upload_complete():
            raise Exception('Upload failed')

        print(f'Publishing...')
        self._publish()
        if not self._is_published():
            raise Exception('Publish failed')

        print(f'Video published/scheduled with id: {self.video["id"]}')

        return self.video['id']

    def _initialize_upload(self):
        url = f"https://graph.facebook.com/v15.0/{self.page_id}/video_reels"
        payload = {
            'upload_phase': 'start',
            'access_token': self.page_access_token
        }
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            self.video['id'] = r.json()['video_id']
        else:
            raise Exception(f'Error initializing upload: {r.json()}')

    def _process_upload(self):
        url = f'https://rupload.facebook.com/video-upload/v15.0/{self.video["id"]}'
        payload = {
            'Authorization': 'OAuth ' + self.page_access_token,
            'offset': '0',
            'file_size': str(self.video['file_size']),
            'Content-Type': 'application/octet-stream'
        }
        requests.post(url, data=self.video['file_data'], headers=payload)

    def _is_upload_complete(self):
        r = self._upload_status()
        return r['status']['uploading_phase']['status'] == 'complete'

    def _upload_status(self):
        url = f'https://graph.facebook.com/v15.0/{self.video["id"]}'
        headers = {
            'Authorization': f'OAuth {self.page_access_token}'
        }
        params = {
            'fields': 'status'
        }

        response = requests.get(url, headers=headers, params=params)

        return response.json()

    def _publish(self):
        url = f"https://graph.facebook.com/v15.0/{self.page_id}/video_reels"

        payload = {
            'access_token': self.page_access_token,
            'video_id': self.video['id'],
            'upload_phase': 'finish',
            'description': self.video['description'],
        }
        if self.video['publish_time']:
            payload['video_state'] = 'SCHEDULED'
            payload['scheduled_publish_time'] = self.video['publish_time']
        else:
            payload['video_state'] = 'PUBLISHED'

        response = requests.post(url, data=payload)

        if response.status_code != 200:
            raise Exception(f'Error publishing video: {response.json()}')

    def _is_published(self):
        reel = self._publish_status()
        return True if reel else False

    def _publish_status(self):
        url = f"https://graph.facebook.com/v15.0/{self.page_id}/video_reels"
        params = {'access_token': self.page_access_token}

        response = requests.get(url, params=params)

        published_reels = response.json()['data']
        published_reel = self._find_reel_by_id(published_reels, self.video['id'])
        return published_reel

    def _find_reel_by_id(self, reels, reel_id):
        for reel in reels:
            if reel['id'] == reel_id:
                return reel
        raise Exception(f'Reel with id {reel_id} not found')
