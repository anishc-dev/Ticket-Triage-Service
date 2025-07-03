import logging
import json
from datetime import datetime

class Log:
    def __init__(self, level, message, **kwargs):
        self.level = level
        self.message = message
        ingest_log(self)


def ingest_log(log):
    json_log = json.dumps(log.__dict__)
    print(json_log) 

def info(message, **kwargs):
    log = Log(logging.INFO, message, **kwargs)

def error(message, **kwargs):
    Log(logging.ERROR, message, **kwargs)