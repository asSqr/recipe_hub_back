# aws/conf.py
# https://medium.com/@kjmczk/s3-heroku-django-faf559c3a401

import os

DEFAULT_FILE_STORAGE = 'recipe_hub_back.aws.utils.MediaRootS3BotoStorage'
# STATICFILES_STORAGE = 'recipe_hub_back.aws.utils.StaticRootS3BotoStorage'

if os.environ.get('AWS_ACCESS_KEY_ID') is not None and os.environ.get('AWS_SECRET_ACCESS_KEY') is not None:
  AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'recipe-hub'  # Amazon S3 のバケット名
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # キャッシュの有効期限（最長期間）= 1日
}
AWS_QUERYSTRING_AUTH = False  # URLからクエリパラメータを削除

AWS_S3_URL = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_URL, 'media')
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_URL, 'static')