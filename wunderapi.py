import wunderclient
import requests
import json

import exceptions as wp_exceptions

DEFAULT_API_URL = 'https://a.wunderlist.com/api'
DEFAULT_API_VERSION='1'

class WunderApi:
    ''' Class to encapsulate all information that could change with API version '''
    def __init__(self, api_url=DEFAULT_API_URL, api_version=DEFAULT_API_VERSION):
        self.api_version = api_version
        self.api_url = api_url
        # All these can change (and likely will) change based on API version in the future
        if api_version:
            class _Endpoints: 
                TASKS = "tasks"
                LISTS = "lists"
                NOTES = "notes"
            self.DATE_FORMAT = '%Y-%m-%d'
            self.DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
            self.MAX_TASK_TITLE_LENGTH = 255
            self.MAX_LIST_TITLE_LENGTH = 255
        self.Endpoints = _Endpoints

    def _validate_response(self, method, response):
        ''' Validates that the response given by Wunderlist is successful, or throw a descriptive error if not '''
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
        Helper to form a request to the Wunderlist API

        method -- GET, PUT, PATCH, etc.
        url_fragment -- trailing portion URL to be appended after the API version
        '''
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

    def get_access_token(self, temporary_code, client_id, client_secret):
        pass

    def get_client(self, access_token, client_id):
        return wunderclient.WunderClient(access_token, client_id, self)
