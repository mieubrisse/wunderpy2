# Represents the Wunderlist data model

# TODO Make all of these variables uppercase, as they're constants!

class _WunderlistObj:
    ID = 'id'
    REVISION = 'revision'

class List(_WunderlistObj):
    ''' POPO to contain list JSON keys '''
    TITLE = 'title'
    CREATION_TIMESTAMP = 'created_at'
    TYPE = 'list_type'
    PUBLIC = 'public'

class Task(_WunderlistObj):
    ''' POPO to contain task JSON keys '''
    ASSIGNEE_ID = 'assignee_id'
    ASSIGNER_ID = 'assigner_id'
    CREATION_TIMESTAMP = 'created_at'
    CREATOR_ID = 'created_by_id'
    DUE_DATE = 'due_date'
    LIST_ID = 'list_id'
    STARRED = 'starred'  # boolean
    TITLE = 'title'
    TYPE = 'type'
    COMPLETED = 'completed' # boolean
    CREATION_REQUEST_ID = 'created_by_request_id'
    RECURRENCE_COUNT = 'recurrence_count'
    RECURRENCE_TYPE = 'recurrence_type'

class Note(_WunderlistObj):
    TASK_ID = 'task_id'
    CREATION_REQUEST_ID = 'createdy_by_request_id'
    TYPE = 'type'   # Always 'note'?
    CONTENT = 'content'

class ReccurrenceTypes():
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR= 'year'
