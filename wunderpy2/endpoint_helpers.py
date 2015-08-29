def get_endpoint_obj(client, endpoint, object_id):
    ''' Tiny helper function that gets used all over the place to join the object ID to the endpoint and run a GET request, returning the result '''
    endpoint = '/'.join([endpoint, str(object_id)])
    return client.authenticated_request(endpoint).json()

def update_endpoint_obj(client, endpoint, object_id, revision, data):
    ''' 
    Helper method to ease the repetitiveness of updating an... SO VERY DRY 
    
    (That's a doubly-effective pun becuase my predecessor - https://github.com/bsmt/wunderpy - found maintaing a Python Wunderlist API to be "as tedious and boring as a liberal arts school poetry slam") 
    '''
    data['revision'] = int(revision)
    endpoint = '/'.join([endpoint, str(object_id)])
    return client.authenticated_request(endpoint, 'PATCH', data=data).json()
