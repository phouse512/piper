import base64
import boto3
import boto3.session
import json
import pytz
import requests
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

    response = requests.post('https://o0ocplke2d.execute-api.us-east-1.amazonaws.com/prod/generate-record',
                             data=json.dumps({'s3_key': s3_key}))

    if response.status_code >= 300:
        print(response)
        raise BaseException("Could not generate record for receipt.")
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': 'this is a really neat test'
    }
