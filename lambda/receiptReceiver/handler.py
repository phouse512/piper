import base64
import boto3
import boto3.session

session = boto3.session.Session(region_name='us-east-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))


def lambda_handler(event, context):
    # TODO implement

    print("body length: %d" % len(event['body']))

    s3client.put_object(
        Body=event['body'],
        Bucket='receipts-storage',
        ContentType='application/pdf',
        Key='test_obj.pdf'
    )
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': 'this is a really neat test'
    }
