# TinychatApiWrapper.py

import logging
import requests
from util import web, Color
from util.response import Response

log = logging.getLogger(__name__)

class TinychatApiWrapper:

    @staticmethod
    def _check_status(response):
        """
        Check the status of the response. Raise an exception if the status is not ok.

        :param response: The response object.
        """
        if not hasattr(response, 'status_code') or not (200 <= response.status_code < 300):
            raise requests.RequestException(
                "HTTP error. Status code: {}".format(response.status_code))

    @staticmethod
    def _write_error(console, error):
        """
        Write error information to the console using the console's write method.
        """
        console.write(error, color=Color.B_RED)

    @classmethod
    def connect_token(cls, room, console):
        url = 'https://tinychat.com/api/v1.0/room/token/{0}'.format(room)

        try:
            web_session = web.WebSession()  # Create a new instance of WebSession
            response = web_session.get(url, as_json=True)
            cls._check_status(response)  # Check for HTTP errors
            response_json = response.json
        except requests.RequestException as e:
            cls._write_error(console, "Error during request: {}".format(e))
            cls._write_error(console, "Exception details: {}".format(e))
            return None
        except ValueError as e:
            cls._write_error(console, "Error decoding JSON: {}".format(e))
            return None

        if 'result' not in response_json:
            cls._write_error(console, "Unexpected response format. Missing 'result' key.")
            return None

        if response_json['result'] != 'success':
            cls._write_error(console, "Failed to retrieve connect token. Result: {}".format(response_json['result']))
            return None

        return {
            'token': response_json.get('result'),
            'endpoint': response_json.get('endpoint')
        }

    @staticmethod
    def _parse_connect_token_response(response, console):
        if response.status_code is None:
            log.error("HTTP error. Status code is None.")
            return None

        if not (200 <= response.status_code < 300):
            log.error("HTTP error. Status code: {}".format(response.status_code))
            return None

        try:
            response_json = response.json
            if 'result' in response_json and response_json['result'] == 'success':
                return {
                    'token': response_json.get('result'),
                    'endpoint': response_json.get('endpoint')
                }
            else:
                log.error("Failed to retrieve connect token. Result: {}".format(response_json.get('result')))
        except Exception as e:
            log.error("Error decoding JSON: {}".format(e))

        return None
