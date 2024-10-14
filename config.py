import json

with open('config.json') as config_file:
    config_jsondata = json.load(config_file)
    uri = config_jsondata['uri']
    username = config_jsondata['username']
    password = config_jsondata['password']
    avatar = config_jsondata['avatar']
    rooms = config_jsondata['rooms']
    prefix = config_jsondata['prefix']
    owner = config_jsondata['owner']
    commands_file = config_jsondata['commands_file']
    remote_repository = config_jsondata['remote_repository']

with open ('db.json') as db_json_file:
    db_jsondata = json.load(db_json_file)
    database = db_jsondata['database']
    host_db = db_jsondata['host']
    user_db = db_jsondata['user']
    password_db = db_jsondata['password']
    port_db = db_jsondata['port']
    schema = db_jsondata['schema']