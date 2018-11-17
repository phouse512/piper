""" account aws lambda handler. """
import json
import logging
import os
from typing import Dict, List

from pony.orm import commit, db_session
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], environment=os.environ["ENV"],
                integrations=[AwsLambdaIntegration()],
                debug=os.environ.get("DEBUG", "false") == "true")

from common.http import HttpResponse
from common.models import Account, Budget

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_handler(event, context) -> Dict:
    """
    Fetch all accounts for a given budget
    :param event: AWSEvent
    :param context: AWSContext
    :return: Dict
    """
    logger.info("Received event: %s", event["queryStringParameters"])

    try:
        budget_id = int(event["queryStringParameters"]["budgetId"])
    except (KeyError, ValueError):
        logger.warning("Bad inputs provided, returning.")
        return HttpResponse(400, message="Invalid input object").to_resp()

    with db_session:
        budget = Budget.select(lambda b: b.id == budget_id)[:]  # type: List[Budget]

        if not budget:
            return HttpResponse(404, message="No budget found for budget id").to_resp()

        accounts = Account.select(lambda a: a.budget_id == budget[0])[:]  # type: List[Account]

    logger.info("Found %s accounts for budget: %s", len(accounts), budget_id)
    return HttpResponse(200, message="Found accounts", body={
        "accounts": [account.to_dict() for account in accounts]
    }).to_resp()


def post_handler(event, context) -> Dict:
    """
    Add a new account for a given budget
    :param event: AWSEvent
    :param context: AWSContext
    :return: Dict
    """
    logger.info("Received input with body: %s", event["body"])

    try:
        input_obj = json.loads(event["body"])

        budget_id = int(input_obj["budgetId"])
        name = str(input_obj["name"])
        assert len(name) > 2
        if "parentId" in input_obj:
            parent_id = int(input_obj["parentId"])
        else:
            parent_id = None
    except Exception as err:
        logger.warning("Bad inputs provided with err: %s", err)
        return HttpResponse(400, message="Invalid input object").to_resp()

    with db_session:
        # check that budget exists
        budget = Budget.select(lambda b: b.id == budget_id)[:]  # type: List[Budget]
        if not budget:
            return HttpResponse(400, message="Bad budget provided").to_resp()

        kwargs = {
            "budget_id": budget[0],
            "name": name,
        }

        if parent_id:
            kwargs["parent_id"] = parent_id

        # insert into accounts
        new_account = Account(**kwargs)
        commit()
        new_account = Account.get(id=new_account.id).to_dict()

    logger.info("Created new account with id: %s", new_account["id"])
    return HttpResponse(200, message="Successfully created", body={
        "account": new_account,
    }).to_resp()
