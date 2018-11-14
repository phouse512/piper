""" budget aws lambda handler. """
import logging
import time
from typing import Dict

from pony.orm import db_session

from common.models import Budget

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_handler(event, context) -> Dict:
    """
    Fetch budget for a person
    :param event: AWSEvent
    :param context: AWSContext
    :return: Dict
    """
    logger.info("Received event: %s", event)

    with db_session:
        budget = Budget.select()[:]
    logger.info(budget[0].home_id)

    return {
        "statusCode": 200,
        "headers": {},
        "body": {},
    }
