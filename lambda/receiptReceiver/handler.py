import base64
import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    # TODO implement

    response = s3.Bucket('receipt-storage').put_object(
        Body=event['body'],
        ContentEncoding='base64',
        ContentType='application/pdf',
        Key='test_obj.pdf'
    )

    print(response)
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': ''
    }
