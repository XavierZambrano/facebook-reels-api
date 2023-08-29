from unittest import TestCase
from unittest.mock import Mock
from facebook_uploader.uploader import FacebookReelsAPI
from facebook_uploader.reel import Reel
from facebook_uploader.exceptions import ReelIdNoneError
from dotenv import load_dotenv
import os


class TestUploader(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.page_id = os.getenv('TEST_PAGE_ID')
        self.page_access_token = os.getenv('TEST_PAGE_ACCESS_TOKEN')

        self.invalid_page_id = 'invalid_page_id'
        self.invalid_page_access_token = 'invalid_page_access_token'

    def test_validate_page_access_token(self):
        self.assertTrue(
            FacebookReelsAPI(
                self.page_id, self.page_access_token
            ).is_page_access_token_valid())

    def test_is_page_access_token_valid_with_invalid_token(self):
        self.assertFalse(
            FacebookReelsAPI(
                self.page_id, self.invalid_page_access_token
            ).is_page_access_token_valid())

    def test_is_page_access_token_valid_with_invalid_page(self):
        self.assertFalse(
            FacebookReelsAPI(
                self.invalid_page_id, self.page_access_token
            ).is_page_access_token_valid())

    def test_is_page_access_token_valid_with_invalid_token_and_page(self):
        self.assertFalse(
            FacebookReelsAPI(
                self.invalid_page_id, self.invalid_page_access_token
            ).is_page_access_token_valid())

    def test_upload_status_reel_id_none(self):
        reels_api = FacebookReelsAPI(self.page_id, self.page_access_token)
        filepath = os.path.join(os.path.dirname(__file__), '../assets/test_vid.mp4')
        reel = Reel(filepath, 'Verdades #frases')
        with self.assertRaises(ReelIdNoneError):
            reels_api.upload_status(reel)

    def test_upload_status(self):
        reels_api = FacebookReelsAPI(self.page_id, self.page_access_token)
        filepath = os.path.join(os.path.dirname(__file__), '../assets/test_vid.mp4')
        reel = Reel(filepath, 'Verdades #frases')

        reels_api._initialize_upload(reel)
        upload_status = reels_api.upload_status(reel, fields=['id', 'updated_time'])
        self.assertEqual(upload_status.keys(), {'id', 'updated_time'})

        upload_status = reels_api.upload_status(reel, fields=['status'])
        self.assertEqual(upload_status.keys(), {'status', 'id'})  # always return id

    def test_json_to_reels(self):
        mock_json = {
            'data': [
                {'description': 'First description', 'updated_time': '2020-01-01T12:00:00+0000', 'id': '11111111111'},
                {'description': 'Second description', 'updated_time': '2020-02-01T12:00:00+0000', 'id': '22222222222'}],
            'paging': {'cursors': {
                'before': 'AAAAAAAAAAAAAAAAA',
                'after': 'BBBBBBBBBBBBBBBBB'}}
        }
        reels_api = FacebookReelsAPI(self.page_id, self.page_access_token)
        reels_api.json = mock_json
        reels = reels_api._json_to_reels()

        self.assertIsInstance(reels, list)
