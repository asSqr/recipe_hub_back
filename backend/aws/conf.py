# aws/conf.py
# https://medium.com/@kjmczk/s3-heroku-django-faf559c3a401

import os

DEFAULT_FILE_STORAGE = 'recipe-hub-back.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'recipe-hub-back.aws.utils.StaticRootS3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')  # 環境変数を指定
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')  # 環境変数を指定

AWS_STORAGE_BUCKET_NAME = '<bucket-name>'  # Amazon S3 のバケット名
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # キャッシュの有効期限（最長期間）= 1日
}
AWS_QUERYSTRING_AUTH = False  # URLからクエリパラメータを削除

AWS_S3_URL = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_URL, 'media')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_URL, 'static')