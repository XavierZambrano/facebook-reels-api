import requests
from facebook_uploader.exceptions import InitializeUploadError, ProcessUploadError, PublishError, ReelIdNoneError
from facebook_uploader.reel import Reel

# api docs https://developers.facebook.com/docs/video-api/guides/reels-publishing


class FacebookReelsAPI:
    def __init__(self, page_id, page_token, api_version: str = 'v17.0'):
        self.page_id = page_id
        self.page_access_token = page_token
        self.api_version = api_version
        self.json = None

    def is_page_access_token_valid(self):
        # /video_reels is to get reels published,
        # but it works to validate the page_access_token
        # and /debug_token requires an app access token
        url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/video_reels"
        params = {
            'since': 'today',
            'access_token': self.page_access_token
        }
        r = requests.get(url, params=params)
        self.json = r.json()
        if r.status_code == 200:
            return True
        else:
            return False

    def upload(self, video: Reel, publish_time=None):
        self._initialize_upload(video)
        self._process_upload(video)
        self._publish(video, publish_time)

        return video.id

    def _initialize_upload(self, video: Reel):
        url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/video_reels"
        payload = {
            'upload_phase': 'start',
            'access_token': self.page_access_token
        }
        r = requests.post(url, data=payload)
        self.json = r.json()
        if r.status_code == 200:
            video.id = r.json()['video_id']
        else:
            raise InitializeUploadError(r.json())

    def _process_upload(self, video):
        url = f'https://rupload.facebook.com/video-upload/{self.api_version}/{video.id}'
        payload = {
            'Authorization': 'OAuth ' + self.page_access_token,
            'offset': '0',
            'file_size': str(video.file_size),
            'Content-Type': 'application/octet-stream'
        }
        r = requests.post(url, data=video.file_data, headers=payload)
        self.json = r.json()
        if r.status_code != 200:
            raise ProcessUploadError(r.json())

    def _publish(self, video, publish_time=None):
        url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/video_reels"

        payload = {
            'access_token': self.page_access_token,
            'video_id': video.id,
            'upload_phase': 'finish',
            'description': video.description,
        }
        if publish_time:
            payload['video_state'] = 'SCHEDULED'
            payload['scheduled_publish_time'] = publish_time
        else:
            payload['video_state'] = 'PUBLISHED'

        r = requests.post(url, data=payload)
        self.json = r.json()
        if r.status_code != 200:
            raise PublishError(r.json())

    def upload_status(self, video: Reel, fields: list[str] = ['status']):
        if video.id is None:
            raise ReelIdNoneError('Initialize upload first')

        url = f'https://graph.facebook.com/{self.api_version}/{video.id}'
        headers = {
            'Authorization': f'OAuth {self.page_access_token}'
        }
        params = {
            'fields': ','.join(fields),
        }

        r = requests.get(url, headers=headers, params=params)
        self.json = r.json()

        return r.json()

    def get_reels(self, since: str | int = None, until: str | int = None):
        url = f'https://graph.facebook.com/{self.api_version}/{self.page_id}/video_reels'
        params = {
            'access_token': self.page_access_token,
            'since': since,
            'until': until
        }
        r = requests.get(url, params=params)
        self.json = r.json()
        reels = self._json_to_reels()
        return reels

    def _json_to_reels(self):
        reels_data = self.json['data']
        reels = []
        for reel_data in reels_data:
            reel = Reel(
                description=reel_data['description'],
                id=reel_data['id'],
                updated_time=reel_data['updated_time']
            )
            reels.append(reel)

        return reels
