import base64
import boto3
import boto3.session
import json
import pytz
import requests
import time
import uuid

from datetime import datetime
from pytz import timezone
from tallyclient import TallyClient

session = boto3.session.Session(region_name='us-west-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))

client = TallyClient("piper.phizzle.space")


def lambda_handler(event, context):
    start_time = time.time()
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

    headers = {'x-api-key': 'oZ67x41VBhaSJ6kPX40BhaqhiDcx9DYC9AZHFX3L'}
    response = requests.post('https://o0ocplke2d.execute-api.us-east-1.amazonaws.com/prod/generate-record',
                             data=json.dumps({'s3_key': s3_key}), headers=headers)

    if response.status_code >= 300:
        print(response.status_code)
        end_time = time.time()
        client.gauge('piper.receiptReceiver.responseTime', int((end_time-start_time) * 1000))
        client.count('piper.receiptReceiver.%s' % response.status_code)
        raise BaseException("Could not generate record for receipt.")

    end_time = time.time()
    client.gauge('piper.receiptReceiver.responseTime', int((end_time-start_time) * 1000))
    client.count('piper.receiptReceiver.200')
    return {
        'statusCode': 200,
        'headers': {},
        'body': 'this is a really neat test'
    }
