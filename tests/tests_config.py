import yaml


# ---- Keys -----
class _CfgKeys:
    CLIENT_ID = "client_id"
    ACCESS_TOKEN = "access_token"
    CLIENT_SECRET = "client_secret"
    ENDPOINT_TESTS = "endpoint_tests"
    TASKS_ENDPOINT = "tasks"
    LISTS_ENDPOINT = "lists"
    NOTES_ENDPOINT = "notes"
    class _EndpointCfgKeys:
        LIST_ID = "list_id"
    class TasksEndpointCfgKeys(_EndpointCfgKeys):
        pass
    class ListsEndpointCfgKeys(_EndpointCfgKeys):
        pass
    class NotesEndpointCfgKeys(_EndpointCfgKeys):
        pass


# ----- Value Extraction ----
# TODO Let user dynamically set the config file!
with open("config.yaml") as config_fp:
    _config_obj = yaml.load(config_fp)

INBOX_ID = _config_obj[_CfgKeys.INBOX_ID]
ACCESS_TOKEN = _config_obj[_CfgKeys.ACCESS_TOKEN]
CLIENT_ID = _config_obj[_CfgKeys.CLIENT_ID]

_tasks_config_obj = _config_obj[_CfgKeys.TASKS_ENDPOINT]
class TasksEndpointCfgValues:
    LIST_ID = _tasks_config_obj[_CfgKeys.TasksEndpointCfgKeys.LIST_ID]

_lists_config_obj = _config_obj[_CfgKeys.LISTS_ENDPOINT]
class ListsEndpointCfgValues:
    LIST_ID = _lists_config_obj[_CfgKeys.ListsEndpointCfgKeys.LIST_ID]

_notes_config_obj = _config_obj[_CfgKeys.NOTES_ENDPOINT]
class NotesEndpointCfgValues:
    LIST_ID = _notes_config_obj[_CfgKeys.NotesEndpointCfgKeys.LIST_ID]
