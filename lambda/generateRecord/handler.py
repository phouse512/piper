import boto3
import json
import os
import psycopg2

from twilio.rest import Client

session = boto3.session.Session(region_name='us-west-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='receiptQueue')


def lambda_handler(event, context):

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    try:
        input_object = json.loads(event['body'])
    except TypeError as e:
        print("Caught error while trying to decode object: %s" % event['body'])
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'message': 'request body was not parseable json'})
        }

    if 's3_key' not in input_object:
        print("S3_key not attached to input body")
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'message': 'request body did not include s3_key as key'})
        }

    # TODO: add s3 head verification

    s3_key = input_object['s3_key']

    insert_record_query = "INSERT INTO records (s3_key) values (%s) RETURNING id"
    cursor.execute(insert_record_query, (s3_key,))
    new_id = cursor.fetchone()[0]
    connection.commit()

    s3_url = s3client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'auto-receipts-storage',
            'Key': s3_key
        }
    )

    response = queue.send_message(MessageBody=json.dumps({'record_id': new_id}))
    print(response)

    # client = Client(os.environ['twilio_account'], os.environ['twilio_token'])
    #
    # client.messages.create(
    #     to="+14403343916",
    #     from_="+14407323016",
    #     body="Received personal receipt, can you help classify?",
    #     media_url=s3_url
    # )

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'record_id': new_id})
    }
