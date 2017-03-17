import boto

# crontab -e
# crontab -l
# dont do this: sudo service cron start

# using json to get the keys
import json
with open('../api_keys.json') as f:
    data = json.load(f)
aws_access_key = data['AWS_ACCESS_KEY_ID']
aws_access_secret_key['AWS_SECRET_ACCESS_KEY']
# scp ~/Desktop/api_keys.json tweets:~


# aws stuff
# import os
# aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
# aws_access_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']

conn = boto.connect_s3(aws_access_key, aws_access_secret_key)

bucket_name = 'urban-emoji-tweets'

b = conn.get_bucket(bucket_name)

file_object = b.new_key('tweets/cron_test.md')#where to save in S3
file_object.set_contents_from_filename('/home/ubuntu/urban-emoji/README.md')
