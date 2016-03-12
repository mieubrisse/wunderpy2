import requests
import sys
import json

from . import model as wp_model
from . import lists_endpoint
from . import tasks_endpoint
from . import notes_endpoint
from . import subtasks_endpoint
from . import positions_endpoints

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
        Send a request to the given Wunderlist API with 'X-Access-Token' and 'X-Client-ID' headers and ensure the response code is as expected given the request type

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
        ''' 
        Gets all notes for the task with the given ID. There will be at most one object in this list; tasks may not have more than one note.

        Returns:
        A list containing one or none Note-mapped objects
        '''
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

        NOTE: A task may have at most one note, so this will fail if a note already exists.
        '''
        return notes_endpoint.create_note(self, task_id, content)

    def update_note(self, note_id, revision, content):
        ''' Updates the note with the given ID to have the given content '''
        return notes_endpoint.update_note(self, note_id, revision, content)

    def delete_note(self, note_id, revision):
        '''
        Deletes the note with the given ID

        NOTE: There is a bug with the API where calling this once will delete the task's note, but then replace it with a new, empty note for the task. To truly delete a task's notes, you must get the note ID of the new, empty note and call this function again on it!

        See https://github.com/wunderlist/api/issues/1
        '''
        notes_endpoint.delete_note(self, note_id, revision)

    def get_task_subtasks(self, task_id, completed=False):
        ''' Gets subtasks for task with given ID '''
        return subtasks_endpoint.get_task_subtasks(self, task_id, completed=completed)

    def get_list_subtasks(self, list_id, completed=False):
        ''' Gets subtasks for the list with given ID '''
        return subtasks_endpoint.get_list_subtasks(self, list_id, completed=completed)

    def get_subtask(self, subtask_id):
        ''' Gets the subtask with the given ID '''
        return subtasks_endpoint.get_subtask(self, subtask_id)

    def create_subtask(self, task_id, title, completed=False):
        ''' 
        Creates a subtask with the given title under the task with the given ID 
        
        Return:
        Newly-created subtask
        '''
        return subtasks_endpoint.create_subtask(self, task_id, title, completed=completed)

    def update_subtask(self, subtask_id, revision, title=None, completed=None):
        '''
        Updates the subtask with the given ID

        See https://developer.wunderlist.com/documentation/endpoints/subtask for detailed parameter information

        Returns:
        Subtask with given ID with properties and revision updated
        '''
        return subtasks_endpoint.update_subtask(self, subtask_id, revision, title=title, completed=completed)

    def delete_subtask(self, subtask_id, revision):
        ''' Deletes the subtask with the given ID '''
        subtasks_endpoint.delete_subtask(self, subtask_id, revision)

    def get_list_positions_objs(self):
        '''
        Gets a list containing the object that encapsulates information about the order lists are laid out in. This list will always contain exactly one object.

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        A list containing a single ListPositionsObj-mapped object
        '''
        return positions_endpoints.get_list_positions_objs(self)

    def get_list_positions_obj(self, positions_obj_id):
        '''
        Gets the object that defines how lists are ordered (there is only one of these)

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        A ListPositionsObj-mapped object defining the order of list layout
        '''
        return positions_endpoints.get_list_positions_obj(self, positions_obj_id)

    def update_list_positions_obj(self, positions_obj_id, revision, values):
        '''
        Updates the ordering of lists to have the given value. The given ID and revision should match the singleton object defining how lists are laid out.

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        The updated ListPositionsObj-mapped object defining the order of list layout
        '''
        return positions_endpoints.update_list_positions_obj(self, positions_obj_id, revision, values)

    def get_task_positions_objs(self, list_id):
        '''
        Gets a list containing the object that controls the order tasks within the list with the given ID are laid out in.  This list will always contain exactly one object, as each list has only one task ordering.

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        A list containing a single TaskPositionsObj-mapped object
        '''
        return positions_endpoints.get_task_positions_objs(self, list_id)

    def get_task_positions_obj(self, positions_obj_id):
        '''
        Gets the object that defines how tasks are ordered within a list (there is one of these per list)

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        A TaskPositionsObj-mapped object defining the order of list layout
        '''
        return positions_endpoints.get_task_positions_obj(self, positions_obj_id)

    def update_task_positions_obj(self, positions_obj_id, revision, values):
        '''
        Updates the ordering of tasks in the positions object with the given ID to the ordering in the given values.

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        The updated TaskPositionsObj-mapped object defining the order of list layout
        '''
        return positions_endpoints.update_task_positions_obj(self, positions_obj_id, revision, values)

    def get_task_subtask_positions_objs(self, task_id):
        '''
        Gets a list containing the object that controls the order subtasks within the task with the given ID are laid out in.  This list will always contain exactly one object, as each task has only one subtask ordering.

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        A list containing a single SubtaskPositionsObj-mapped object
        '''
        return positions_endpoints.get_task_subtask_positions_objs(self, task_id)

    def get_list_subtask_positions_objs(self, list_id):
        '''
        Gets all subtask positions objects for the tasks within a given list. This is a convenience method avoid needing to get all the list's tasks before getting subtasks.

        Returns:
        List of SubtaskPositionsObj-mapped objects representing the order of subtasks for the tasks within the given list
        '''
        return positions_endpoints.get_list_subtask_positions_objs(self, list_id)

    def get_subtask_positions_obj(self, positions_obj_id):
        '''
        Gets the object that defines how subtasks are ordered within a task (there is one of these per task)

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        A SubtaskPositionsObj-mapped object defining the order of subtask layout
        '''
        return positions_endpoints.get_subtask_positions_obj(self, positions_obj_id)

    def update_subtask_positions_obj(self, positions_obj_id, revision, values):
        '''
        Updates the ordering of subtasks in the positions object with the given ID to the ordering in the given values.

        See https://developer.wunderlist.com/documentation/endpoints/positions for more info

        Return:
        The updated SubtaskPositionsObj-mapped object defining the order of list layout
        '''
        return positions_endpoints.update_subtask_positions_obj(self, positions_obj_id, revision, values)

