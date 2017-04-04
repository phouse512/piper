import base64
import boto3
import boto3.session

session = boto3.session.Session(region_name='us-east-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))


def lambda_handler(event, context):
    # TODO implement

    s3client.put_object(
        Bucket='receipts-storage',
        ContentEncoding='base64',
        ContentType='application/pdf',
        Key='test_obj.pdf'
    )
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': ''
    }
