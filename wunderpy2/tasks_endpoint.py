import datetime

'''
Encapsulates all tasks that can be run against the 'tasks' endpoint
'''
def _check_title_length(title, api):
    ''' Checks the given title against the given API specifications to ensure it's short enough '''
    if len(title) > api.MAX_TASK_TITLE_LENGTH:
        raise ValueError("Title cannot be longer than {} characters".format(api.MAX_TASK_TITLE_LENGTH))

def _check_date_format(date, api):
    ''' Checks that the given date string conforms to the given API's date format specification '''
    try:
        datetime.datetime.strptime(date, api.DATE_FORMAT)
    except ValueError:
        raise ValueError("Date '{}' does not conform to API format: {}".format(date, api.DATE_FORMAT))

def get_tasks(client, list_id, completed=False):
    ''' Gets un/completed tasks for the given list ID '''
    params = { 
            'list_id' : str(list_id), 
            'completed' : completed 
            }
    response = client.authenticated_request(client.api.Endpoints.TASKS, params=params)
    return response.json()

def get_task(client, task_id):
    ''' Gets task information for the given ID '''
    endpoint = '/'.join([client.api.Endpoints.TASKS, str(task_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_task(client, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None):
    ''' 
    Creates a task in the given list 

    See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
    '''
    _check_title_length(title, client.api)
    if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
        raise ValueError("recurrence_type and recurrence_count are required are required together")
    if due_date is not None:
        _check_date_format(due_date, client.api)
    data = {
            'list_id' : int(list_id) if list_id else None,
            'title' : title,
            'assignee_id' : int(assignee_id) if assignee_id else None,
            'completed' : completed,
            'recurrence_type' : recurrence_type,
            'recurrence_count' : int(recurrence_count) if recurrence_count else None,
            'due_date' : due_date,
            'starred' : starred,
            }
    data = { key: value for key, value in data.items() if value is not None }
    response = client.authenticated_request(client.api.Endpoints.TASKS, 'POST', data=data)
    return response.json()

def update_task(client, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None):
    '''
    Updates the task with the given ID

    See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
    '''
    if title is not None:
        _check_title_length(title, client.api)
    if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
        raise ValueError("recurrence_type and recurrence_count are required are required together")
    if due_date is not None:
        _check_date_format(due_date, client.api)
    data = {
            'revision' : int(revision),
            'title' : title,
            'assignee_id' : int(assignee_id) if assignee_id else None,
            'completed' : completed,
            'recurrence_type' : recurrence_type,
            'recurrence_count' : int(recurrence_count) if recurrence_count else None,
            'due_date' : due_date,
            'starred' : starred,
            'remove' : remove,
            }
    data = { key: value for key, value in data.items() if value is not None }
    endpoint = '/'.join([client.api.Endpoints.TASKS, str(task_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.json()

def delete_task(client, task_id, revision):
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.TASKS, str(task_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)
