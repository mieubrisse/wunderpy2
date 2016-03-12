import requests
import json

from . import wunderclient
from . import exceptions as wp_exceptions

ACCESS_TOKEN_URL = 'https://www.wunderlist.com/oauth/access_token'
DEFAULT_API_URL = 'https://a.wunderlist.com/api'
DEFAULT_API_VERSION='1'

class WunderApi:
    ''' Class to encapsulate all information that could change with API version '''
    def __init__(self, api_url=DEFAULT_API_URL, api_version=DEFAULT_API_VERSION):
        self.api_version = api_version
        self.api_url = api_url
        # All these can (and likely will) change based on API version in the future
        if api_version:
            class _Endpoints: 
                TASKS = "tasks"
                LISTS = "lists"
                NOTES = "notes"
                SUBTASKS = "subtasks"
                LIST_POSITIONS = "list_positions"
                TASK_POSITIONS = "task_positions"
                SUBTASK_POSITIONS = "subtask_positions"

            self.DATE_FORMAT = '%Y-%m-%d'
            self.DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
            self.MAX_TASK_TITLE_LENGTH = 255
            self.MAX_LIST_TITLE_LENGTH = 255
            self.MAX_SUBTASK_TITLE_LENGTH = 255
        self.Endpoints = _Endpoints

    def _validate_response(self, method, response):
        ''' Helper method to validate the given to a Wunderlist API request is as expected '''
        # TODO Fill this out using the error codes here: https://developer.wunderlist.com/documentation/concepts/formats
        # The expected results can change based on API version, so validate this here
        if self.api_version:
            if response.status_code >= 400:
                raise ValueError('{} {}'.format(response.status_code, str(response.json())))
            if method == 'GET':
                assert response.status_code == 200
            elif method == 'POST':
                assert response.status_code == 201
            elif method == 'PATCH':
                assert response.status_code == 200
            elif method == 'DELETE':
                assert response.status_code == 204

    def request(self, endpoint, method='GET', headers=None, params=None, data=None):
        '''
        Send a request to the given Wunderlist API endpoint

        Params:
        endpoint -- API endpoint to send request to

        Keyword Args:
        headers -- headers to add to the request
        method -- GET, PUT, PATCH, DELETE, etc.
        params -- parameters to encode in the request
        data -- data to send with the request
        '''
        if not headers:
            headers = {}
        if method in ['POST', 'PATCH', 'PUT']:
            headers['Content-Type'] = 'application/json'
        url = '/'.join([self.api_url, 'v' + self.api_version, endpoint])
        data = json.dumps(data) if data else None
        try:
            response = requests.request(method=method, url=url, params=params, headers=headers, data=data)
        # TODO Does recreating the exception classes 'requests' use suck? Yes, but it sucks more to expose the underlying library I use
        except requests.exceptions.Timeout as e:
            raise wp_exceptions.TimeoutError(e)
        except requests.exceptions.ConnectionError as e:
            raise wp_exceptions.ConnectionError(e)
        self._validate_response(method, response)
        return response

    def get_access_token(self, code, client_id, client_secret):
        ''' 
        Exchange a temporary code for an access token allowing access to a user's account

        See https://developer.wunderlist.com/documentation/concepts/authorization for more info
        '''
        headers = {
                'Content-Type' : 'application/json'
                }
        data = {
                'client_id' : client_id,
                'client_secret' : client_secret,
                'code' : code,
                }
        str_data = json.dumps(data)
        response = requests.request(method='POST', url=ACCESS_TOKEN_URL, headers=headers, data=str_data)
        status_code = response.status_code
        if status_code != 200:
            raise ValueError("{} -- {}".format(status_code, response.json()))
        return body['access_token']

    def get_client(self, access_token, client_id):
        ''' Gets a client with the given access token and ID pointing to this API '''
        return wunderclient.WunderClient(access_token, client_id, self)
