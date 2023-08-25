import requests

# api docs https://developers.facebook.com/docs/video-api/guides/reels-publishing
# TODO check why only me can see the reels, and why don't get views

class FacebookReelsUploader:
    def __init__(self, page_id, page_token):
        self.page_id = page_id
        self.page_access_token = page_token
        self.video = None

    def upload(self, video, publish_time=None):
        hashtags = ' '.join([f'#{tag}' for tag in video["tags"]])
        video_description_with_hashtags = f'{video["description"]} {hashtags}'

        video['video_id'] = None
        video['file_data'] = open(video['file_path'], 'rb')
        video['description'] = video_description_with_hashtags
        video['publish_time'] = publish_time
        self.video = video

        self._initialize_upload()
        print(f'Upload initialized with id: {self.video["id"]}')
        self._process_upload()  # Resume file upload if interrupted
        self._upload_status()
        self._publish()
        self._upload_status()
        self._publish_status()

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
        }
        requests.post(url, data=self.video['file_data'], headers=payload)

    def _upload_status(self):
        # TODO What happens if the upload is interrupted? How to resume it?
        url = f'https://graph.facebook.com/v15.0/{self.video["id"]}'
        headers = {
            'Authorization': f'OAuth {self.page_access_token}'
        }
        params = {
            'fields': 'status'
        }

        response = requests.get(url, headers=headers, params=params)
        # TODO If response.json()["uploading_phase"] == "in_progress" OR != complete, the load must be resumed
        print(f'upload_status: {response.json()}')

    def _publish(self):
        url = f"https://graph.facebook.com/v15.0/{self.page_id}/video_reels"

        payload = {
            'access_token': self.page_access_token,
            'video_id': self.video['id'],
            'upload_phase': 'finish',
            # 'title': self.video['title'],
            'description': self.video['description'],
        }
        if self.video['publish_time']:
            payload['video_state'] = 'SCHEDULED'
            payload['scheduled_publish_time'] = self.video['publish_time']
        else:
            payload['video_state'] = 'PUBLISHED'

        response = requests.post(url, data=payload)
        print(response.json())
        if response.status_code != 200:
            raise Exception(f'Error publishing video: {response.json()}')

    def _publish_status(self):
        url = f"https://graph.facebook.com/v15.0/{self.page_id}/video_reels"
        params = {'access_token': self.page_access_token}

        response = requests.get(url, params=params)

        published_reels = response.json()['data']
        published_reel = self._find_reel_by_id(published_reels, self.video['id'])
        print(f'publish_status: {published_reel}')

    def _find_reel_by_id(self, reels, reel_id):
        for reel in reels:
            if reel['id'] == reel_id:
                return reel
        raise Exception(f'Reel with id {reel_id} not found')
