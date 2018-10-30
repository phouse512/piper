""" Handles incoming dynamodb stream items. """
import json
import logging
import os
import time
from typing import Dict, List

import boto3
from botocore.config import Config
import botocore.exceptions
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)

sentry_sdk.init(dsn=os.environ["SENTRY_DSN"],
                environment=os.environ["ENV"],
                integrations=[AwsLambdaIntegration()])

config = Config(  # pylint: disable=invalid-name
    connect_timeout=5,
    read_timeout=5,
    retries={"max_attempts": 0},
)

if os.environ.get("AWS_PROFILE", ""):
    session = boto3.Session(  # pylint: disable=invalid-name
        profile_name=os.environ["AWS_PROFILE"],
    )
else:
    session = boto3.Session()  # pylint: disable=invalid-name

firehose_client = session.client(  # pylint: disable=invalid-name
    config=config,
    service_name="firehose",
)


def store_batch(records: List[Dict], retry_count: int = 0) -> List:
    """
    Stores a list of generic records
    :param records: List[Dict]
    :param retry_count: int, defaults to 0
    :return: List[Dict], any failed records
    """
    if retry_count > 2:
        logger.warning("Hit retry limit, returning %s failed records", len(records))
        return records

    try:
        response = firehose_client.put_record_batch(
            DeliveryStreamName=os.environ["FIREHOSE_NAME"],
            Records=[
                {
                    "Data": "{},".format(json.dumps(obj).encode("utf-8")),
                } for obj in records
            ]
        )
    except (botocore.exceptions.ConnectTimeoutError, botocore.exceptions.ReadTimeoutError) as err:
        logger.warning("firehose put batch timed out with: %s", err)
        return store_batch(records, retry_count=retry_count+1)
    except botocore.exceptions.ClientError as err:
        error = err.response["Error"]["Code"]
        if error == "ServiceUnavailable":
            logger.warning("firehose service not available, waiting some time")
            time.sleep(5)
            return store_batch(records, retry_count=retry_count+1)

        logger.warning("Received uncaught aws error: %s - will retry", error)
        time.sleep(3)
        return store_batch(records, retry_count=retry_count+1)

    # check for individual failed puts and add those independently
    failed_count = response["FailedPutCount"]
    if failed_count < 1:
        logger.info("Successfully put all %s records, returning", len(records))
        return []

    to_retry = []  # list of failed records to retry
    # loop through and find the failed ones
    for idx, response in enumerate(response["RequestResponses"]):
        if "ErrorCode" in response:
            logger.warning("Individual record failed with error: %s and message: %s",
                           response["ErrorCode"], response["ErrorMessage"])
            to_retry.append(records[idx])

    logger.warning("%s records failed to store, retrying if under limit", len(to_retry))
    return store_batch(to_retry, retry_count=retry_count+1)


def handler(event, context):  # pylint: disable=unused-argument
    """
    Handler method that is responsible for putting dynamodb data into firehose
    :param event: AWSEvent
    :param context: AWSContext
    :return: None
    """
    try:
        records = event["Records"]

        for record in records:
            if record["eventSource"] != "aws:dynamodb":
                raise Exception("Unknown source type..")
    except Exception as err:
        logger.error("Unable to parse records with err: %s", err)
        raise err

    # firehose batch input
    start = int(time.time() * 1000)
    failed_records = store_batch(records)
    logger.info("Firehose batch store took %sms", int(time.time() * 1000) - start)

    if failed_records:
        logger.error("TO_RETRY_RECORDS: %s", len(failed_records))
        for record in failed_records:
            logger.error("RECORD: %s", json.dumps(record))

        raise Exception("All records failed to store successfully.")
