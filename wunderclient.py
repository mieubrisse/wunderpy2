import requests
import sys
import json

import model as wp_model
import lists_endpoint
import tasks_endpoint
import notes_endpoint

class WunderClient:
    # TODO Factor our these methods into subclasses, for easier logical organization
    ''' Client for accessing the Wunderlist info of a user (given by the access token) '''

    def __init__(self, access_token, client_id, api):
        '''
        Create a Wunderlist client with the given parameters.

        Params:
        access_token -- Wunderlist access token, given once a user has given Wunderlist permission access their data
        client_id -- Wunderlist-generated ID for the app accessing the client's data
        api -- WunderApi handle to API information
        '''
        self.client_id = client_id
        self.access_token = access_token
        self.api = api

    def authenticated_request(self, endpoint, method='GET', params=None, data=None):
        '''
        Send a request to the given Wunderlist API with 'X-Access-Token' and 'X-Client-ID' headers

        Params:
        endpoint -- API endpoint to send request to

        Keyword Args:
        method -- GET, PUT, PATCH, DELETE, etc.
        params -- parameters to encode in the request
        data -- data to send with the request
        '''
        headers = {
                'X-Access-Token' : self.access_token,
                'X-Client-ID' : self.client_id
                }
        return self.api.request(endpoint, method=method, headers=headers, params=params, data=data)

    def get_lists(self):
        return lists_endpoint.get_lists(self)

    def get_list(self, list_id):
        return lists_endpoint.get_list(self, list_id)

    def create_list(self, title):
        return lists_endpoint.create_list(self, title)

    def update_list(self, list_id, revision, title=None, public=None):
        return lists_endpoint.update_list(self, list_id, revision, title=title, public=public)

    def delete_list(self, list_id, revision):
        lists_endpoint.delete_list(self, list_id, revision)

    def get(self, list_id, completed=False):
        return task_endpoint.get(self, list_id, completed=False)

    def get_task(self, task_id):
        return task_endpoint.get_task(self, task_id)

    def create_task(self, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None):
        return task_endpoint.create_task(self, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None)

    def update_task(self, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None):
        return task_endpoint.update_task(self, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None)

    def delete_task(self, task_id, revision):
        task_endpoint.delete_task(self, task_id, revision)

    def get_task_notes(self, task_id):
        return notes_endpoint.get_task_notes(self, task_id)

    def get_list_notes(self, list_id):
        return notes_endpoint.get_list_notes(self, list_id)

    def get_note(self, note_id):
        return notes_endpoint.get_note(self, note_id)

    def create_note(self, task_id, content):
        return notes_endpoint.create_note(self, task_id, content)

    def update_note(self, note_id, revision, content):
        return notes_endpoint.update_note(self, note_id, revision, content)

    def delete_note(self, note_id, revision):
        notes_endpoint.delete_note(self, note_id, revision)
