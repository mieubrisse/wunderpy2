'''
Encapsulates all tasks that can be run against the 'notes' endpoint
'''
def get_task_notes(client, task_id):
    params = {
            'task_id' : int(task_id)
            }
    response = client.authenticated_request(client.api.Endpoints.NOTES, params=params)
    assert response.status_code == 200
    return response.json()

def get_list_notes(client, list_id):
    params = {
            'list_id' : int(list_id)
            }
    response = client.authenticated_request(client.api.Endpoints.NOTES, params=params)
    assert response.status_code == 200
    return response.json()

def get_note(client, note_id):
    endpoint = '/'.join([client.api.Endpoints.NOTES, str(note_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_note(client, task_id, content):
    data = {
            'task_id' : int(task_id),
            'content' : content,
            }
    response = client.authenticated_request(client.api.Endpoints.NOTES, method='POST', data=data)
    return response.json()

def update_note(client, note_id, revision, content):
    data = {
            'revision': int(revision),
            'content': content,
            }
    endpoint = '/'.join([client.api.Endpoints.NOTES, str(note_id)])
    response = client.authenticated_request(endpoint, method='PATCH', data=data)
    return response.json()

def delete_note(client, note_id, revision):
    # NOTE There is a bug in the Wunderlist API where this must be called twice in order for the note to actually be deleted - once on the note you want deleted and once on the new, empty, replacement note that gets generated
    params = {
            'revision' : revision
            }
    endpoint = '/'.join([client.api.Endpoints.NOTES, str(note_id)])
    response = client.authenticated_request(endpoint, method='DELETE', params=params)
