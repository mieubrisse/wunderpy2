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
        ''' Gets all the user's lists '''
        return lists_endpoint.get_lists(self)

    def get_list(self, list_id):
        ''' Gets information about the list with the given ID '''
        return lists_endpoint.get_list(self, list_id)

    def create_list(self, title):
        ''' Creates a new list with the given title '''
        return lists_endpoint.create_list(self, title)

    def update_list(self, list_id, revision, title=None, public=None):
        ''' Updates the list with the given ID to have the given title and public flag '''
        return lists_endpoint.update_list(self, list_id, revision, title=title, public=public)

    def delete_list(self, list_id, revision):
        ''' Deletes the list with the given ID '''
        lists_endpoint.delete_list(self, list_id, revision)

    def get_tasks(self, list_id, completed=False):
        ''' Gets tasks for the list with the given ID, filtered by the given completion flag '''
        return tasks_endpoint.get_tasks(self, list_id, completed=completed)

    def get_task(self, task_id):
        ''' Gets information about the task with the given ID '''
        return tasks_endpoint.get_task(self, task_id)

    def create_task(self, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None):
        ''' Creates a new task with the given information in the list with the given ID '''
        return tasks_endpoint.create_task(self, list_id, title, assignee_id=assignee_id, completed=completed, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date, starred=starred)

    def update_task(self, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None):
        ''' 
        Updates the task with the given ID to have the given information 
        
        NOTE: The 'remove' parameter is an optional list of parameters to remove from the given task, e.g. ['due_date']
        '''
        return tasks_endpoint.update_task(self, task_id, revision, title=title, assignee_id=assignee_id, completed=completed, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date, starred=starred, remove=remove)

    def delete_task(self, task_id, revision):
        ''' Deletes the task with the given ID '''
        tasks_endpoint.delete_task(self, task_id, revision)

    def get_task_notes(self, task_id):
        ''' Gets all notes for the task with the given ID '''
        return notes_endpoint.get_task_notes(self, task_id)

    def get_list_notes(self, list_id):
        ''' Gets all notes for the list with the given ID '''
        return notes_endpoint.get_list_notes(self, list_id)

    def get_note(self, note_id):
        ''' Gets information about the note with the given ID '''
        return notes_endpoint.get_note(self, note_id)

    def create_note(self, task_id, content):
        ''' 
        Creates a new note for the task with the given ID

        NOTE: Fails if a note already exists
        '''
        return notes_endpoint.create_note(self, task_id, content)

    def update_note(self, note_id, revision, content):
        ''' Updates the note with the given ID to have the given content '''
        return notes_endpoint.update_note(self, note_id, revision, content)

    def delete_note(self, note_id, revision):
        '''
        Deletes the note with the given ID

        NOTE: There is a bug/feature with the API where calling this once will delete the task's note, but then replace it with a new, empty note for the task. To truly delete a task's notes, you must get the note ID of the new, empty note and call this function again on it
        '''
        notes_endpoint.delete_note(self, note_id, revision)
