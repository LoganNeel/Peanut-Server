from functools import wraps
import os
from flask import request
from flask.cli import load_dotenv

load_dotenv()

ROOT_KEY = os.getenv('ROOT_KEY')
DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')

if not ROOT_KEY or not DEVELOPER_KEY:
    raise ValueError('ROOT_KEY and DEVELOPER_KEY must be set in environment variables.')

def requires_root_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('root-key') != ROOT_KEY:
            return {'error': 'Unauthorized. Requires root.'}, 401
        return f(*args, **kwargs)
    return decorated_function

def requires_developer_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('developer-key') != DEVELOPER_KEY:
            return {'error': 'Unauthorized. Requires developer.'}, 401
        return f(*args, **kwargs)
    return decorated_function