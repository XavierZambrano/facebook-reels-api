from unittest import TestCase
from facebook_uploader.uploader import FacebookReelsAPI
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
