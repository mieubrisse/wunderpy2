# Represents the Wunderlist data model

# TODO Make all of these variables uppercase, as they're constants!

class _WunderlistObj:
    id = 'id'
    revision = 'revision'

class List(_WunderlistObj):
    ''' POPO to contain list JSON keys '''
    title = 'title'
    creation_timestamp = 'created_at'
    type = 'list_type'
    public = 'public'

class Task(_WunderlistObj):
    ''' POPO to contain task JSON keys '''
    assignee_id = 'assignee_id'
    assigner_id = 'assigner_id'
    creation_timestamp = 'created_at'
    creator_id = 'created_by_id'
    due_date = 'due_date'
    list_id = 'list_id'
    starred = 'starred'  # boolean
    title = 'title'
    type = 'type'
    completed = 'completed' # boolean
    creation_request_id = 'created_by_request_id'
    recurrence_count = 'recurrence_count'
    recurrence_type = 'recurrence_type'

class Note(_WunderlistObj):
    TASK_ID = 'task_id'
    CREATION_REQUEST_ID = 'createdy_by_request_id'
    TYPE = 'type'   # Always 'note'?
    CONTENT = 'content'

class ReccurrenceTypes():
    day = 'day'
    week = 'week'
    month = 'month'
    year= 'year'
