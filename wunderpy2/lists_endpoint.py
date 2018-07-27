'''
Encapsulates all tasks that can be run against the 'lists' endpoint
'''
def _check_title_length(title, api):
    ''' Checks the given title against the given API specifications to ensure it's short enough '''
    if len(title) > api.MAX_LIST_TITLE_LENGTH:
        raise ValueError("Title cannot be longer than {} characters".format(api.MAX_TASK_TITLE_LENGTH))

def get_lists(client):
    ''' Gets all the client's lists '''
    response = client.authenticated_request(client.api.Endpoints.LISTS)
    return response.json()

def get_list(client, list_id):
    ''' Gets the given list '''
    endpoint = '/'.join([client.api.Endpoints.LISTS, str(list_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_list(client, title):
    ''' Creates a new list with the given title '''
    _check_title_length(title, client.api)
    data = {
            'title' : title,
            }
    response = client.authenticated_request(client.api.Endpoints.LISTS, method='POST', data=data)
    return response.json()

def update_list(client, list_id, revision, title=None, public=None):
    '''
    Updates the list with the given ID to have the given properties

    See https://developer.wunderlist.com/documentation/endpoints/list for detailed parameter information
    '''
    if title is not None:
        _check_title_length(title, client.api)
    data = {
            'revision' : revision,
            'title' : title,
            'public' : public,
            }
    data = { key: value for key, value in data.items() if value is not None }
    endpoint = '/'.join([client.api.Endpoints.LISTS, str(list_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.json()

def delete_list(client, list_id, revision):
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.LISTS, str(list_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)

