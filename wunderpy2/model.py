# Represents the Wunderlist data model

# TODO Potentially make these actual classes and parse the JSON we get back from Wunderlist so we can hand the users classes to work with (intead of dicts)? Looked at the 'colander' module for this, but it didn't really do anything more than's being done right now...

class _WunderlistObj:
    ''' Basic block of all Wunderlist communication '''
    ID = 'id'
    REVISION = 'revision'

class _WunderlistEntity(_WunderlistObj):
    ''' Entity with creation timestamp properties '''
    # NOTE these may be null for certain things, like the inbox
    CREATION_REQUEST_ID = 'created_by_request_id'
    CREATION_TIMESTAMP = 'created_at'
    CREATED_BY_ID = 'created_by_id'

class List(_WunderlistEntity):
    ''' POPO to contain list JSON keys '''
    TITLE = 'title'
    OWNER_ID = 'owner_id'
    OWNER_TYPE = 'owner_type'  # Seems to always be 'user'
    TYPE = 'list_type'
    PUBLIC = 'public'

class Task(_WunderlistEntity):
    ''' POPO to contain task JSON keys '''
    ASSIGNEE_ID = 'assignee_id'
    ASSIGNER_ID = 'assigner_id'
    DUE_DATE = 'due_date'
    LIST_ID = 'list_id'
    STARRED = 'starred'  # boolean
    TITLE = 'title'
    TYPE = 'type'
    COMPLETED = 'completed' # boolean
    RECURRENCE_COUNT = 'recurrence_count'
    RECURRENCE_TYPE = 'recurrence_type'

class Subtask(_WunderlistEntity):
    ''' POJO Containing subtask JSON keys '''
    TITLE = 'title'
    TASK_ID = 'task_id'
    COMPLETED = 'completed'
    TYPE = 'type'

# NOTE Wunderlist automatically creates positions objects, so they don't have creation information
class _PositionsObj(_WunderlistObj):
    VALUES = 'values'
    TYPE = 'type'

class ListPositionsObj(_PositionsObj):
    pass

class TaskPositionsObj(_PositionsObj):
    LIST_ID = 'list_id'

class SubtaskPositionsObj(_PositionsObj):
    TASK_ID = 'task_id'

class Note(_WunderlistObj):
    # NOTE Notes don't seem to get any creation info: user, timestamp, or request
    TASK_ID = 'task_id'
    TYPE = 'type'   # Always 'note'?
    CONTENT = 'content'

class RecurrenceTypes():
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR= 'year'
