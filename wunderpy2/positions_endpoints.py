'''
Encapsulates all tasks that can be run against the 'positions' endpoint

In my unprofessional opinion, this API could use some reworking: positions objects seem to be singletons, but you can get lists of them for some reason
'''

from . import endpoint_helpers

def _update_positions_obj(client, endpoint, positions_obj_id, revision, values):
    data = {
            'values' : values,
            }
    return endpoint_helpers.update_endpoint_obj(client, endpoint, positions_obj_id, revision, data)

# NOTE The Wunderlist API does a poor job of naming objects here. The objects containing the order for list objects are called list_position objects, when really the list positions are what are reflected in the containing object. I'll think of a better name for these.
def get_list_positions_objs(client):
    '''
    Gets a list containing the object that encapsulates information about the order lists are laid out in. This list will always contain exactly one object.

    See https://developer.wunderlist.com/documentation/endpoints/positions for more info

    Return:
    A list containing a single ListPositionsObj-mapped object
    '''
    return client.authenticated_request(client.api.Endpoints.LIST_POSITIONS).json()

def get_list_positions_obj(client, positions_obj_id):
    '''
    Gets the object that defines how lists are ordered (there will always be only one of these)

    See https://developer.wunderlist.com/documentation/endpoints/positions for more info

    Return:
    A ListPositionsObj-mapped object defining the order of list layout
    '''
    return endpoint_helpers.get_endpoint_obj(client, client.api.Endpoints.LIST_POSITIONS, positions_obj_id)

# TODO Is user_id the right value????
def update_list_positions_obj(client, positions_obj_id, revision, values):
    '''
    Updates the ordering of lists to have the given value. The given ID and revision should match the singleton object defining how lists are laid out.

    See https://developer.wunderlist.com/documentation/endpoints/positions for more info

    Return:
    The updated ListPositionsObj-mapped object defining the order of list layout
    '''
    return _update_positions_obj(client, client.api.Endpoints.LIST_POSITIONS, positions_obj_id, revision, values)

def get_task_positions_objs(client, list_id):
    '''
    Gets a list containing the object that encapsulates information about the order lists are laid out in. This list will always contain exactly one object.

    See https://developer.wunderlist.com/documentation/endpoints/positions for more info

    Return:
    A list containing a single ListPositionsObj-mapped object
    '''
    params = {
            'list_id' : int(list_id)
            }
    response = client.authenticated_request(client.api.Endpoints.TASK_POSITIONS, params=params)
    return response.json()

def get_task_positions_obj(client, positions_obj_id):
    return endpoint_helpers.get_endpoint_obj(client, client.api.Endpoints.TASK_POSITIONS, positions_obj_id)

def update_task_positions_obj(client, positions_obj_id, revision, values):
    return _update_positions_obj(client, client.api.Endpoints.TASK_POSITIONS, positions_obj_id, revision, values)

def get_task_subtask_positions_objs(client, task_id):
    '''
    Gets a list of the positions of a single task's subtasks

    Each task should (will?) only have one positions object defining how its subtasks are laid out
    '''
    params = {
            'task_id' : int(task_id)
            }
    response = client.authenticated_request(client.api.Endpoints.SUBTASK_POSITIONS, params=params)
    return response.json()

# NOTE Lists don't have subtasks; this is just a convenience method to see all the subtask positions objects for all the tasks in a list
def get_list_subtask_positions_objs(client, list_id):
    '''
    Gets all subtask positions objects for the tasks within a given list. This is a convenience method so you don't have to get all the list's tasks before getting subtasks, though I can't fathom how mass subtask reordering is useful.

    Returns:
    List of SubtaskPositionsObj-mapped objects representing the order of subtasks for the tasks within the given list
    '''
    params = {
            'list_id' : int(list_id)
            }
    response = client.authenticated_request(client.api.Endpoints.SUBTASK_POSITIONS, params=params)
    return response.json()

def get_subtask_positions_obj(client, positions_obj_id):
    return endpoint_helpers.get_endpoint_obj(client, client.api.Endpoints.SUBTASK_POSITIONS, positions_obj_id)

def update_subtask_positions_obj(client, positions_obj_id, revision, values):
    return _update_positions_obj(client, client.api.Endpoints.SUBTASK_POSITIONS, positions_obj_id, revision, values)
    

