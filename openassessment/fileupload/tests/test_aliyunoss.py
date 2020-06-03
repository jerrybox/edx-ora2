# -*- coding: utf-8 -*-

from urlparse import urlparse

from mock import Mock, patch

from django.test import TestCase
from django.test.utils import override_settings

from openassessment.fileupload import api


@override_settings(
    ORA2_FILEUPLOAD_BACKEND='aliyunoss',
    OSS_ENDPOINT='http://www.example.com:12345',
    OSS_ACCESS_KEY_ID='aliyun_access_key_id',
    OSS_ACCESS_KEY_SECRET='aliyun_access_key_secret',
    FILE_UPLOAD_STORAGE_BUCKET_NAME='bucket_name'
)
class TestAliyunossBackend(TestCase):
    """
    Test open assessment file upload to swift object storage.
    """
    def setUp(self):
        super(TestAliyunossBackend, self).setUp()
        self.backend = api.backends.get_backend()

    def _verify_url(self, url):
        result = urlparse(url)
        self.assertEqual(result.scheme, u'http')
        self.assertEqual(result.netloc, u'bucket_name.www.example.com:12345')
        self.assertEqual(result.path, u'/submissions_attachments/foo')
        self.assertIn(result.params, 'OSSAccessKeyId=')
        self.assertIn(result.params, 'Expires=')
        self.assertIn(result.params, 'Signature=')

    def test_get_backend(self):
        """
        Verify that there are no errors setting up aliyunoss as a backend.
        """
        self.assertTrue(isinstance(self.backend, api.backends.aliyunoss.Backend))

    def test_get_upload_url(self):
        """
        Verify the upload URL.
        """
        url = self.backend.get_upload_url('foo', '_text')
        self._verify_url(url)

    @patch('openassessment.fileupload.backends.aliyunoss.requests.get')
    def test_get_download_url_success(self, requests_get_mock):
        """
        Verify the download URL when the object already exists in storage.
        """
        fake_resp = Mock()
        fake_resp.status_code = 200  # always return a 200 status code
        requests_get_mock.return_value = fake_resp
        url = self.backend.get_download_url('foo')
        self._verify_url(url)

    @patch('openassessment.fileupload.backends.aliyunoss.requests.get')
    def test_get_download_url_no_object(self, requests_get_mock):
        """
        Verify the download URL is empty when the object
        cannot be found in storage.
        """
        fake_resp = Mock()
        fake_resp.status_code = 404  # always return a 404 status code
        requests_get_mock.return_value = fake_resp
        url = self.backend.get_download_url('foo')
        self.assertEqual(url, '')
