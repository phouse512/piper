""" budget aws lambda handler. """
import logging
import os
from typing import Dict, List

from pony.orm import db_session
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], environment=os.environ["ENV"],
                integrations=[AwsLambdaIntegration()],
                debug=os.environ.get("DEBUG", "false") == "true")

from common.http import HttpResponse
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
    logger.info("Received event with params: %s", event["pathParameters"])

    try:
        budget_id = int(event["pathParameters"]["id"])
    except (KeyError, ValueError):
        logger.warning("Bad inputs, 400ing")
        return HttpResponse(400, message="Invalid input object").to_resp()

    with db_session:
        budget = Budget.select(lambda b: b.id == budget_id)[:]  # type: List[Budget]

    if not budget:
        logger.warning("No budget found for id.")
        return HttpResponse(404, message="No budget found for id.").to_resp()

    logger.info("Found budget with name: %s", budget[0].name)

    return HttpResponse(200, message="Found budget", body={
        "budget": budget[0].to_dict(),
    }).to_resp()
