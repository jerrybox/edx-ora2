# -*- coding: utf-8 -*-
"""
Note1: Both  cms and lms need to be configured.
Note2: aliyunoss configure  Access-Control-Allow-Origin

vim /edx/app/edxapp/lms.env.json
+ "ORA2_FILEUPLOAD_BACKEND": "aliyunoss",

vim /edx/app/edxapp/lms.auth.json
+ "ALIYUN_OSS_ENDPOINT":null,
+ "ALIYUN_ACCESS_KEY_ID":null,
+ "ALIYUN_ACCESS_KEY_SECRET":null,

cat  /edx/app/edxapp/edx-platform/lms/envs/common.py | grep FILE_UPLOAD_STORAGE_BUCKET_NAME
FILE_UPLOAD_STORAGE_BUCKET_NAME = 'edxuploads'

vim /edx/app/edxapp/edx-platform/lms/envs/aws.py +/AUTH_TOKENS

###############################aliyunoss#######################
ORA2_FILEUPLOAD_BACKEND = ENV_TOKENS.get("ORA2_FILEUPLOAD_BACKEND")

ALIYUN_OSS_ENDPOINT = AUTH_TOKENS.get("ALIYUN_OSS_ENDPOINT")
ALIYUN_ACCESS_KEY_ID = AUTH_TOKENS.get("ALIYUN_ACCESS_KEY_ID")
ALIYUN_ACCESS_KEY_SECRET = AUTH_TOKENS.get("ALIYUN_ACCESS_KEY_SECRET")

vim /edx/app/edxapp/cms.env.json +/FILE_UPLOAD_STORAGE_BUCKET_NAME
FILE_UPLOAD_STORAGE_BUCKET_NAME = 'edxuploads'

"""
import logging

import oss2

from django.conf import settings

from ..exceptions import FileUploadInternalError
from .base import BaseBackend

logger = logging.getLogger("openassessment.fileupload.api")


class Backend(BaseBackend):

    ALIYUN_OSS_ENDPOINT = getattr(settings, 'ALIYUN_OSS_ENDPOINT', None)

    def get_upload_url(self, key, content_type):
        bucket_name, key_name = self._retrieve_parameters(key)
        try:
            auth = _auth_to_aliyunoss()
            bucket = oss2.Bucket(auth, self.ALIYUN_OSS_ENDPOINT, bucket_name)
            sign_url = bucket.sign_url(
                'PUT',
                key_name,
                self.UPLOAD_URL_TIMEOUT,
                headers={'Content-Type': content_type}
            )
            return sign_url
        except Exception as ex:
            logger.exception(
                u"An internal exception occurred while generating an upload URL."
            )
            raise FileUploadInternalError(ex)

    def get_download_url(self, key):
        bucket_name, key_name = self._retrieve_parameters(key)
        try:
            auth = _auth_to_aliyunoss()
            bucket = oss2.Bucket(auth, self.ALIYUN_OSS_ENDPOINT, bucket_name)

            file_exist = bucket.object_exists(key_name)
            if file_exist:
                sign_url = bucket.sign_url(
                    'GET',
                    key_name,
                    self.UPLOAD_URL_TIMEOUT
                )
                return sign_url
            else:
                return ""
        except Exception as ex:
            logger.exception(
                u"An internal exception occurred while generating a download URL."
            )
            raise FileUploadInternalError(ex)

    def remove_file(self, key):
        bucket_name, key_name = self._retrieve_parameters(key)
        auth = _auth_to_aliyunoss()
        bucket = oss2.Bucket(auth, self.ALIYUN_OSS_ENDPOINT, bucket_name)
        file_exist = bucket.object_exists(key_name)
        if file_exist:
            try:
                response = bucket.delete_object(key_name)
                return True
            except oss2.exceptions.NoSuchKey as e:
                return True
        else:
            return False


def _auth_to_aliyunoss():
    """Connect to aliyunoss

    Creates a connection to aliyunoss for file URLs.

    """
    # Try to get the AWS credentials from settings if they are available
    # If not, these will default to `None`, and boto will try to use
    # environment vars or configuration files instead.
    aliyun_aws_access_key_id = getattr(settings, 'ALIYUN_ACCESS_KEY_ID', None)
    aliyun_aws_access_key_secret = getattr(settings, 'ALIYUN_ACCESS_KEY_SECRET', None)

    return oss2.Auth(aliyun_aws_access_key_id, aliyun_aws_access_key_secret)
