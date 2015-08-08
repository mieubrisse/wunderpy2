import urllib3
import requests
import sys
import json
import model
import wunderpy2.exceptions

def _ensure_not_empty(params):
    ''' Check that the values in the given dict of (pretty param name -> value) is not None or empty. '''
    for pretty_name, value in params.iteritems():
        if value is None or not value.strip():
            raise ValueError('{} cannot be null or empty'.format(pretty_name))

def _validate_response(response):
    ''' Validates that the response given by Wunderlist is successful, or throw a descriptive error if not '''
    # TODO Fill this out using the error codes here: https://developer.wunderlist.com/documentation/concepts/formats
    if response.status_code >= 400:
        raise ValueError('{} {}'.format(response.status_code, str(response.json())))

# All times are UTC time
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
API_URL = 'https://a.wunderlist.com/api'
MAX_TASK_TITLE_LENGTH = 255

class _Endpoints:
    tasks = "tasks"
    lists = "lists"

class WunderClient:
    ''' Client for accessing the Wunderlist info of a user (given by the access token) '''

    def __init__(self, access_token, client_id, api_version='1'):
        '''
        Create a Wunderlist client with the given parameters.

        access_token -- Wunderlist access token, given once a user has given Wunderlist permission access their data
        client_id -- Wunderlist-generated ID for the app accessing the client's data

        Keyword args:
        api_version -- Version of the Wunderlist API
        '''

        # Sanity checks
        _ensure_not_empty({ 'access token' : access_token, 'client_id' : client_id })

        self.client_id = client_id
        self.access_token = access_token
        self.api_version = api_version

    def _wunderlist_request(self, endpoint, method='GET', params=None, data=None):
        '''
        Helper to form a request to the Wunderlist API

        method -- GET, PUT, PATCH, etc.
        url_fragment -- trailing portion URL to be appended after the API version
        '''
        headers = {
                'X-Access-Token' : self.access_token,
                'X-Client-ID' : self.client_id
                }
        if method in ['POST', 'PATCH', 'PUT']:
            headers['Content-Type'] = 'application/json'
        url = '/'.join([API_URL, 'v' + self.api_version, endpoint])
        data = json.dumps(data) if data else None
        try:
            response = requests.request(method=method, url=url, params=params, headers=headers, data=data)
        # TODO Does recreating the exception classes 'requests' use suck? Yes, but it sucks more to expose the underlying library I use
        except requests.exceptions.TimeoutError as e:
            raise wunderpy2.exceptions.TimeoutError(e)
        except requests.exceptions.ConnectionError as e:
            raise wunderpy2.exceptions.ConnectionError(e)
        _validate_response(response)
        return response

    def get_lists(self):
        ''' Gets all the client's lists '''
        response = self._wunderlist_request(_Endpoints.lists)
        return response.json()

    def get_list(self, list_id):
        ''' Gets the given list '''
        endpoint = '/'.join([_Endpoints.lists, str(list_id)])
        response = self._wunderlist_request(endpoint)
        return response.json()

    def create_list(self, title):
        # TODO https://developer.wunderlist.com/documentation/endpoints/list
        pass

    def update_list(self, new_list_obj, revision):
        # TODO https://developer.wunderlist.com/documentation/endpoints/list
        pass

    def make_list_public(self, list_id, revision):
        # TODO https://developer.wunderlist.com/documentation/endpoints/list
        pass

    def delete_list(self, list_id, revision):
        # TODO https://developer.wunderlist.com/documentation/endpoints/list
        pass

    def get_tasks(self, list_id, completed=False):
        ''' Gets un/completed tasks for the given list ID '''
        params = { model.Task.list_id : str(list_id), model.Task.completed : completed }
        response = self._wunderlist_request(_Endpoints.tasks, params=params)
        return response.json()

    def get_task(self, task_id):
        ''' Gets task information for the given ID '''
        endpoint = '/'.join([_Endpoints.tasks, str(task_id)])
        response = self._wunderlist_request(endpoint)
        return response.json()

    def create_task(self, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None):
        ''' 
        Creates a task in the given list 

        See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
        '''
        if len(title) > MAX_TASK_TITLE_LENGTH:
            raise ValueError("Title cannot be longer than {} characters".format(MAX_TASK_TITLE_LENGTH))
        if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
            raise ValueError("recurrence_type and recurrence_count are required are required together")
        data = {
                model.Task.list_id : int(list_id) if list_id else None,
                model.Task.title : title,
                model.Task.assignee_id : int(assignee_id) if assignee_id else None,
                model.Task.completed : completed,
                model.Task.recurrence_type : recurrence_type,
                model.Task.recurrence_count : int(recurrence_count) if recurrence_count else None,
                model.Task.due_date : due_date,
                model.Task.starred : starred,
                }
        data = { key: value for key, value in data.iteritems() if value is not None }
        response = self._wunderlist_request(_Endpoints.tasks, 'POST', data=data)
        return response.json()

    def update_task(self, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None):
        '''
        Updates the task with the given ID

        See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
        '''
        if len(title) > MAX_TASK_TITLE_LENGTH:
            raise ValueError("Title cannot be longer than {} characters".format(MAX_TASK_TITLE_LENGTH))
        if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
            raise ValueError("recurrence_type and recurrence_count are required are required together")
        data = {
                model.Task.title : title,
                model.Task.assignee_id : int(assignee_id) if assignee_id else None,
                model.Task.completed : completed,
                model.Task.recurrence_type : recurrence_type,
                model.Task.recurrence_count : int(recurrence_count) if recurrence_count else None,
                model.Task.due_date : due_date,
                model.Task.starred : starred,
                model.Task.revision : int(revision),
                'remove' : remove,
                }
        data = { key: value for key, value in data.iteritems() if value is not None }
        endpoint = '/'.join([_Endpoints.tasks, str(task_id)])
        response = self._wunderlist_request(endpoint, 'PATCH', data=data)
        return response.json()

    def delete_task(self, task_id, revision):
        params = {
                model.Task.revision : int(revision),
                }
        endpoint = '/'.join([_Endpoints.tasks, str(task_id)])
        response = self._wunderlist_request(endpoint, 'DELETE', params=params)
        assert response.status_code == 204

if __name__ == '__main__':
    client = WunderClient(sys.argv[1], sys.argv[2])
    lists = client.get_lists()
    list_id = lists[0][model.List.id]
    tasks = client.get_tasks(list_id, completed=False)
    task_id = tasks[0][model.Task.id]
    print json.dumps(tasks)

