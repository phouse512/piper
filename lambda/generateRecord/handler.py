import boto3
import json
import os
import psycopg2

session = boto3.session.Session(region_name='us-west-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))


def lambda_handler(event, context):

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    input_object = json.loads(event['body'])

    # insert_record_query =

    return {
        'statusCode': 200,
        'headers': {},
        'body': 'this is a really neat test'
    }
