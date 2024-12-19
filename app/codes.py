from flask import jsonify


OK = 0
ERROR_UNKNOWN = 1
ERROR_FILE_NOT_FOUND = 2
ERROR_FILE_EXISTS = 3
ERROR_INVALID_TRACK = 4
ERROR_INVALID_VERSION = 5

def get_json_error_response(code: int) -> tuple[str, int]:
    """
    Returns a JSON error response and the corresponding HTTP status code.
    """
    messages = {
        OK: 'OK',
        ERROR_UNKNOWN: 'Unknown error',
        ERROR_FILE_NOT_FOUND: 'File not found',
        ERROR_FILE_EXISTS: 'File already exists',
        ERROR_INVALID_TRACK: 'Invalid track',
        ERROR_INVALID_VERSION: 'Invalid versions'
    }
    if code == OK:
        return jsonify({'error': 'OK'}), 200

    return (jsonify({'error': messages[code]}), 400) if code in messages else (jsonify({'error': 'Unknown error'}), 500)