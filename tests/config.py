import yaml

class ConfigKeys:
    CLIENT_ID = "client_id"
    ACCESS_TOKEN = "access_token"
    CLIENT_SECRET = "client_secret"
    INBOX_ID = "inbox_id"

def load_config(config_filepath):
    with open(config_filepath) as config_fp:
        return yaml.load(config_fp)
