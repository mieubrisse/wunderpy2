import requests
import sys
import json

import model as wp_model

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
        return self.api.request(endpoint, method=method, headers=headers, params=params, data=data)


    def get_lists(self):
        ''' Gets all the client's lists '''
        response = self.authenticated_request(self.api.Endpoints.LISTS)
        return response.json()

    def get_list(self, list_id):
        ''' Gets the given list '''
        endpoint = '/'.join([self.api.Endpoints.LISTS, str(list_id)])
        response = self.authenticated_request(endpoint)
        return response.json()

    def create_list(self, title):
        ''' Creates a new list with the given title '''
        if len(title) > self.api.MAX_LIST_TITLE_LENGTH:
            raise ValueError("Title cannot be longer than {} characters".format(self.api.MAX_LIST_TITLE_LENGTH))
        data = {
                'title' : title,
                }
        response = self.authenticated_request(self.api.Endpoints.LISTS, method='POST', data=data)
        return response.json()

    def update_list(self, list_id, revision, title=None, public=None):
        '''
        Updates the list with the given ID to have the given properties

        See https://developer.wunderlist.com/documentation/endpoints/list for detailed parameter information
        '''
        if len(title) > self.api.MAX_LIST_TITLE_LENGTH:
            raise ValueError("Title cannot be longer than {} characters".format(self.api.MAX_LIST_TITLE_LENGTH))
        data = {
                'revision' : revision,
                'title' : title,
                'public' : public,
                }
        data = { key: value for key, value in data.iteritems() if value is not None }
        endpoint = '/'.join([self.api.Endpoints.LISTS, str(list_id)])
        response = self.authenticated_request(endpoint, 'PATCH', data=data)
        return response.json()

    def delete_list(self, list_id, revision):
        params = {
                'revision' : int(revision),
                }
        endpoint = '/'.join([self.api.Endpoints.LISTS, str(list_id)])
        self.authenticated_request(endpoint, 'DELETE', params=params)

    def get_tasks(self, list_id, completed=False):
        ''' Gets un/completed tasks for the given list ID '''
        params = { 
                wp_model.Task.list_id : str(list_id), 
                wp_model.Task.completed : completed 
                }
        response = self.authenticated_request(self.api.Endpoints.TASKS, params=params)
        return response.json()

    def get_task(self, task_id):
        ''' Gets task information for the given ID '''
        endpoint = '/'.join([self.api.Endpoints.TASKS, str(task_id)])
        response = self.authenticated_request(endpoint)
        return response.json()

    def create_task(self, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None):
        ''' 
        Creates a task in the given list 

        See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
        '''
        if len(title) > self.api.MAX_TASK_TITLE_LENGTH:
            raise ValueError("Title cannot be longer than {} characters".format(self.api.MAX_TASK_TITLE_LENGTH))
        if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
            raise ValueError("recurrence_type and recurrence_count are required are required together")
        data = {
                wp_model.Task.list_id : int(list_id) if list_id else None,
                wp_model.Task.title : title,
                wp_model.Task.assignee_id : int(assignee_id) if assignee_id else None,
                wp_model.Task.completed : completed,
                wp_model.Task.recurrence_type : recurrence_type,
                wp_model.Task.recurrence_count : int(recurrence_count) if recurrence_count else None,
                wp_model.Task.due_date : due_date,
                wp_model.Task.starred : starred,
                }
        data = { key: value for key, value in data.iteritems() if value is not None }
        response = self.authenticated_request(self.api.Endpoints.TASKS, 'POST', data=data)
        assert response.status_code == 201
        return response.json()

    def update_task(self, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None):
        '''
        Updates the task with the given ID

        See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
        '''
        if len(title) > self.api.MAX_TASK_TITLE_LENGTH:
            raise ValueError("Title cannot be longer than {} characters".format(self.api.MAX_TASK_TITLE_LENGTH))
        if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
            raise ValueError("recurrence_type and recurrence_count are required are required together")
        data = {
                wp_model.Task.title : title,
                wp_model.Task.assignee_id : int(assignee_id) if assignee_id else None,
                wp_model.Task.completed : completed,
                wp_model.Task.recurrence_type : recurrence_type,
                wp_model.Task.recurrence_count : int(recurrence_count) if recurrence_count else None,
                wp_model.Task.due_date : due_date,
                wp_model.Task.starred : starred,
                wp_model.Task.revision : int(revision),
                'remove' : remove,
                }
        data = { key: value for key, value in data.iteritems() if value is not None }
        endpoint = '/'.join([self.api.Endpoints.TASKS, str(task_id)])
        response = self.authenticated_request(endpoint, 'PATCH', data=data)
        return response.json()

    def delete_task(self, task_id, revision):
        params = {
                wp_model.Task.revision : int(revision),
                }
        endpoint = '/'.join([self.api.Endpoints.TASKS, str(task_id)])
        self.authenticated_request(endpoint, 'DELETE', params=params)

    def get_task_note(self, task_id):
        params = {
                'task_id' : int(task_id)
                }
        response = self.authenticated_request(self.api.Endpoints.NOTES, params=params)
        assert response.status_code == 200
        return response.json()

    def get_list_notes(self, list_id):
        params = {
                'list_id' : int(list_id)
                }
        response = self.authenticated_request(self.api.Endpoints.NOTES, params=params)
        assert response.status_code == 200
        return response.json()

    def get_note(self, note_id):
        endpoint = '/'.join([self.api.Endpoints.NOTES, str(note_id)])
        response = self.authenticated_request(endpoint)
        return response.json()

    def create_note(self, task_id, content):
        data = {
                'task_id' : int(task_id),
                'content' : content,
                }
        response = self.authenticated_request(self.api.Endpoints.NOTES, method='POST', data=data)
        return response.json()

    def update_note(self, note_id, revision, content):
        data = {
                'revision': int(revision),
                'content': content,
                }
        endpoint = '/'.join([self.api.Endpoints.NOTES, str(note_id)])
        response = self.authenticated_request(endpoint, method='PATCH', data=data)
        return response.json()

    def delete_note(self, note_id, revision):
        # NOTE There is a bug in the Wunderlist API where this must be called twice in order for the note to actually be deleted - once on the note you want deleted and once on the new, empty, replacement note that gets generated
        params = {
                'revision' : revision
                }
        endpoint = '/'.join([self.api.Endpoints.NOTES, str(note_id)])
        response = self.authenticated_request(endpoint, method='DELETE', params=params)

if __name__ == '__main__':
    client = WunderClient(sys.argv[1], sys.argv[2])
    lists = client.get_lists()
    list_id = lists[0][wp_model.List.id]
    tasks = client.get_tasks(list_id, completed=False)
    task_id = tasks[0][wp_model.Task.id]
    print json.dumps(tasks)

