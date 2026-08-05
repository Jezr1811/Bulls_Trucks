import os

from storages.backends.s3 import S3Storage


class MediaStorage(S3Storage):
    bucket_name = os.getenv("R2_BUCKET_NAME")
    default_acl = None
    file_overwrite = False
    custom_domain = os.getenv("AWS_S3_CUSTOM_DOMAIN", None)
    querystring_auth = False