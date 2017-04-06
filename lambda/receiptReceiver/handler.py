import base64
import boto3
import boto3.session
import pytz
import uuid

from datetime import datetime
from pytz import timezone

session = boto3.session.Session(region_name='us-west-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))


def lambda_handler(event, context):

    print("body length: %d" % len(event['body']))
    print("first part of string: %s" % event['body'][:100])

    current_date = datetime.now().replace(tzinfo=pytz.UTC)
    date_string = current_date.astimezone(timezone('US/Pacific')).strftime("%b-%y")

    s3_key = "%s/%s.pdf" % (date_string.lower(), uuid.uuid4())

    s3client.put_object(
        Body=base64.b64decode(event['body']),
        Bucket='auto-receipts-storage',
        ContentType='application/pdf',
        Key=s3_key
    )
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': 'this is a really neat test'
    }
