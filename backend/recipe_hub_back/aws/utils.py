# aws/utils.py
# https://medium.com/@kjmczk/s3-heroku-django-faf559c3a401

from storages.backends.s3boto3 import S3Boto3Storage
 
def MediaRootS3BotoStorage(): return S3Boto3Storage(location='media')
def StaticRootS3BotoStorage(): return S3Boto3Storage(location='static')