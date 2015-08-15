import yaml

# ----- Value Extraction ----
# TODO Let user dynamically set the config file!
with open("tests_config.yaml") as config_fp:
    _config_obj = yaml.load(config_fp)

ACCESS_TOKEN = _config_obj["access_token"]
CLIENT_ID = _config_obj["client_id"]
CLIENT_SECRET = _config_obj["client_secret"]


# ---- Config values for testing endpoints ------
_endpoint_tests_obj = _config_obj["endpoint_tests"]

# tasks
_tasks_config_obj = _endpoint_tests_obj["tasks"]
class TasksEndpointCfgValues:
    LIST_ID = _tasks_config_obj["list_id"]

# lists
_lists_config_obj = _endpoint_tests_obj["lists"]
class ListsEndpointCfgValues:
    LIST_ID = _lists_config_obj["list_id"]

# notes
_notes_config_obj = _endpoint_tests_obj["notes"]
class NotesEndpointCfgValues:
    LIST_ID = _notes_config_obj["list_id"]
    TASK_ID_WITH_NOTES = _notes_config_obj["task_id_with_notes"]
    TASK_ID_WITHOUT_NOTES = _notes_config_obj["task_id_without_notes"]
    NOTE_ID = _notes_config_obj["note_id"]
