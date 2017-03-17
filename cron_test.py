import boto
import os

# crontab -e
# sudo service cron start

# aws stuff
aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_access_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']



conn = boto.connect_s3(aws_access_key, aws_access_secret_key)

bucket_name = 'urban-emoji-tweets'

b = conn.get_bucket(bucket_name)

file_object = b.new_key('tweets/cron_test.md')#where to save
file_object.set_contents_from_filename('README.md')
