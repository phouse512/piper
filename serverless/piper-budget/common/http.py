""" Holds the methods/decorators that are used for interfacing with API Gateway. """
import json
from typing import Any, Dict, Type


class HttpResponse(object):  # pylint: disable=too-few-public-methods
    """ Custom HTTP class that is used to return objects that API gateway uses to return. """

    def __init__(self, status_code: int = 400, headers: Dict = None, message: str = "",
                 body: Any = None) -> None:
        """
        Construct a HttpResponse object.
        :param status_code: int, HTTP status code. see http://bit.ly/1ZKo4EE
        :param headers: Dict of headers, defaults to empty
        :param message: str, status message with info
        :param body: optional body
        """
        default_headers = {"Access-Control-Allow-Origin": "*",
                           "Access-Control-Allow-Headers": "piper-key",
                           "Access-Control-Allow-Credentials": True}
        if headers:
            default_headers.update(headers)

        self.status_code = status_code
        self.headers = default_headers
        self.message = message
        self.body = body

    def to_resp(self, encoder: Type[json.JSONEncoder] = None) -> Dict:
        """
        Returns a dictionary formatted for API gateway output standard.
        :return: Dict
        """
        kwargs = {}
        if encoder:
            kwargs["cls"] = encoder

        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": json.dumps({
                "message": self.message,
                "data": self.body,
            }, **kwargs)
        }
