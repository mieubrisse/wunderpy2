'''
Encapsulates all tasks that can be run against the 'subtasks' endpoint
'''

def _check_title_length(title, api):
    ''' Checks the given title against the given API specifications to ensure it's short enough '''
    if len(title) > api.MAX_SUBTASK_TITLE_LENGTH:
        raise ValueError("Title cannot be longer than {} characters".format(api.MAX_SUBTASK_TITLE_LENGTH))

def get_task_subtasks(client, task_id, completed=False):
    ''' Gets subtasks for task with given ID '''
    params = {
            'task_id' : int(task_id),
            'completed' : completed,
            }
    response = client.authenticated_request(client.api.Endpoints.SUBTASKS, params=params)
    return response.json()

def get_list_subtasks(client, list_id, completed=False):
    ''' Gets subtasks for the list with given ID '''
    params = {
            'list_id' : int(list_id),
            'completed' : completed,
            }
    response = client.authenticated_request(client.api.Endpoints.SUBTASKS, params=params)
    return response.json()

def get_subtask(client, subtask_id):
    ''' Gets the subtask with the given ID '''
    endpoint = '/'.join([client.api.Endpoints.SUBTASKS, str(subtask_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_subtask(client, task_id, title, completed=False):
    ''' Creates a subtask with the given title under the task with the given ID '''
    _check_title_length(title, client.api)
    data = {
            'task_id' : int(task_id) if task_id else None,
            'title' : title,
            'completed' : completed,
            }
    data = { key: value for key, value in data.items() if value is not None }
    response = client.authenticated_request(client.api.Endpoints.SUBTASKS, 'POST', data=data)
    return response.json()

def update_subtask(client, subtask_id, revision, title=None, completed=None):
    '''
    Updates the subtask with the given ID

    See https://developer.wunderlist.com/documentation/endpoints/subtask for detailed parameter information
    '''
    if title is not None:
        _check_title_length(title, client.api)
    data = {
            'revision' : int(revision),
            'title' : title,
            'completed' : completed,
            }
    data = { key: value for key, value in data.items() if value is not None }
    endpoint = '/'.join([client.api.Endpoints.SUBTASKS, str(subtask_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.json()

def delete_subtask(client, subtask_id, revision):
    ''' Deletes the subtask with the given ID provided the given revision equals the revision the server has '''
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.SUBTASKS, str(subtask_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)
