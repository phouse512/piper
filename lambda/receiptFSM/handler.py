import boto3
import json
import os
import psycopg2
import urlparse

from datetime import datetime
from twilio.rest import Client

session = boto3.session.Session(region_name='us-west-1')
s3client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))

STATES = ['idle', 'sent_pdf', 'received_from', 'received_to']


def get_next(current):
    """
    iterates through states to find the next state
    :param current: string of current state
    :return: string of next state
    """
    for index,value in enumerate(STATES):
        if value == current:
            if index == len(STATES)-1:
                return STATES[0]
            else:
                return STATES[index+1]


class State(object):

    def __init__(self, user_id, state, record_id, phone, created_at):
        self.user_id = user_id
        self.state = state
        self.record_id = record_id
        self.phone = phone
        self.created_at = created_at

    @staticmethod
    def from_db_row(row):
        """
        row: [user_id, state, record_id, phone, created_at]
        """
        return State(row[0], row[1], row[2], row[3], row[4])


def advance_state(current_state, cursor, connection, record_id=None):
    """

    :param current_state: State object representing current state
    :param cursor: psycopg2 cursor
    :param connection: psycopg2 connection
    :param record_id: integer representing record, can be None
    :return:
    """

    if not record_id:
        record_id = -1

    next_state = get_next(current_state.state)

    advance_state_query = "INSERT INTO receipts_fsm (user_id, state, record_id, phone) values " \
                          "(%s, %s, %s, %s)"
    cursor.execute(advance_state_query, (current_state.user_id, next_state, record_id, current_state.phone,))
    connection.commit()


def to_sent_pdf(new_record, current_state, cursor, connection, twilio_client):
    """
    :param new_record: integer that indicates the new record to process
    :param current_state: State object that represents current fsm state
    :param cursor: psycopg2 cursor
    :param connection: psycopg2 connection
    :param twilio_client: Client object from the Twilio library
    :return:
    """

    record_query = "SELECT s3_key FROM records WHERE id=%s"
    cursor.execute(record_query, (new_record,))
    s3_key = cursor.fetchone()[0]

    s3_url = s3client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'auto-receipts-storage',
            'Key': s3_key
        }
    )

    twilio_client.messages.create(
        to=current_state.phone,
        from_="+14407323016",
        body="Received personal receipt, from where is this money coming from?",
        media_url=s3_url
    )

    advance_state(current_state, cursor, connection, new_record)


def lambda_handler(event, context):
    print(event['body'])

    # logic to determine if coming from generateRecord or twilio
    if 'Piper-Internal' in event['headers'] and event['headers']['Piper-Internal'] == 'true':
        try:
            input_object = json.loads(event['body'])
        except TypeError as e:
            print("Caught error while trying to decode object: %s" % event['body'])
            return {
                'statusCode': 400,
                'headers': {},
                'body': json.dumps({'message': 'request body was not parseable json'})
            }
    else:
        # this is coming from twilio, parse as query params
        try:
            input_object = urlparse.parse_qs(event['body'])
        except Exception as e:
            print("Caught error while trying to url parse object: %s" % event['body'])
            return {
                'statusCode': 400,
                'headers': {},
                'body': json.dumps({'message': 'request body was not parseable query params'})
            }

    client = Client(os.environ['twilio_account'], os.environ['twilio_token'])

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    latest_state_query = "SELECT user_id, state, record_id, phone, created_at FROM receipts_fsm " \
                         "WHERE user_id=%s ORDER BY created_at DESC LIMIT 1"
    cursor.execute(latest_state_query, (1,))
    current_state = State.from_db_row(cursor.fetchone())

    if current_state.state == 'idle':
        if 'record_id' not in input_object:
            return {
                'statusCode': 400,
                'headers': {},
                'body': json.dumps({'message': 'record_id not included for idle state'})
            }

        to_sent_pdf(int(input_object['record_id']), current_state, cursor, connection, client)

        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({'message': 'Successfully notified.'})
        }

    elif current_state.state == 'sent_pdf':
        print("sent pdf state")
        print(input_object['Body'][0])
    elif current_state.state == 'received_from':
        print("sent received from")
    elif current_state.state == 'received_to':
        print("received_do")
    else:
        print('invalid state')

    return {
        'statusCode': 200,
        'headers': {},
        'body': 'this is a really neat test'
    }
