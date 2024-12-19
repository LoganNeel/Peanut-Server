from app.codes import get_json_error_response
from app.decorators import requires_root_access, requires_developer_access
from flask import Flask, request, jsonify, make_response

from app.files import (create_project_folder, delete_project_folder, get_project_ids, upload_file_to_project,
                       delete_file_from_project, get_project_config_dict, get_project_files_json, get_file_bytes,
                       get_autoupdater_xml_content, get_project_ids_with_track, create_project_branch, does_track_exist)
app = Flask(__name__)

@app.route('/projects/<project_id>', methods=['POST'])
@requires_root_access
def post_project(project_id: str):
    result: int = create_project_folder(project_id)
    return jsonify({'message': 'Project created successfully'}) if result == 0 else get_json_error_response(result)

@app.route('/projects/<project_id>/<track>', methods=['POST'])
@requires_root_access
def post_project_branch(project_id: str, track: str):
    result: int = create_project_branch(project_id, track)
    return jsonify({'message': 'Project branch created successfully'}) if result == 0 else get_json_error_response(result)
@app.route('/projects', methods=['GET'])
def get_projects():
    project_ids, code = get_project_ids()
    return (jsonify({'projects': project_ids}), 200) if not code else get_json_error_response(code)

@app.route('/projects/branches', methods=['GET'])
def get_projects_with_branches():
    project_ids, code = get_project_ids_with_track()
    return (jsonify({'projects': project_ids}), 200) if not code else get_json_error_response(code)

@app.route('/projects/<project_id>', methods=['DELETE'])
@requires_root_access
def delete_project(project_id: str):
    result: int = delete_project_folder(project_id)
    return jsonify({'message': 'Project deleted successfully'}) if not result else get_json_error_response(result)

@app.route('/projects/<project_id>/upload/<track>', methods=['POST'])
@requires_developer_access
def upload_file(project_id: str, track: str):
    if not does_track_exist(project_id, track):
        return jsonify({'error': 'Invalid track. Must be develop or main.'}), 400
    
    try:
        file_data = request.files['file']
        file_name = file_data.filename
        file_bytes = file_data.read()
        result: int = upload_file_to_project(project_id, track, file_name, file_bytes)
    except Exception:
        return jsonify({'error': 'Invalid request body'}), 400

    return jsonify({'message': 'File uploaded successfully'}) if not result else get_json_error_response(result)

@app.route('/projects/<project_id>/upload/<track>/<file_id>', methods=['DELETE'])
@requires_developer_access
def delete_file(project_id: str, track: str, file_id: str):
    result: int = delete_file_from_project(project_id, track, file_id)
    return jsonify({'message': 'File deleted successfully'}) if result == 0 else get_json_error_response(result)

@app.route('/apps/<project_id>/config.json', methods=['GET'])
def get_project_config(project_id: str):
    dictionary, code = get_project_config_dict(project_id, 'main')
    return (jsonify(dictionary), 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/files', methods=['GET'])
def get_project_files(project_id: str):
    file_data, code = get_project_files_json(project_id, 'main')
    return (jsonify(file_data), 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/<develop>/files', methods=['GET'])
@requires_developer_access
def get_project_files_develop(project_id: str, track:str):
    file_data, code = get_project_files_json(project_id, track)
    return (jsonify(file_data), 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/latest', methods=['GET'])
def get_latest(project_id: str):
    dictionary, code = get_project_config_dict(project_id, 'main')
    if code: 
        return get_json_error_response(code)
    data, code = get_file_bytes(project_id, 'main', dictionary['latest_file'])
    return (data, 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/<develop>/latest', methods=['GET'])
def get_latest_develop(project_id: str, track:str):
    dictionary, code = get_project_config_dict(project_id, track)
    if code: 
        return get_json_error_response(code)
    data, code = get_file_bytes(project_id, 'develop', dictionary['latest_file'])
    return (data, 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/autoupdater.xml', methods=['GET'])
def get_autoupdater_xml(project_id: str):
    content, code = get_autoupdater_xml_content(project_id, 'main')
    return (content, 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/<develop>/autoupdater.xml', methods=['GET'])
def get_autoupdater_xml_develop(project_id: str, track:str,):
    content, code = get_autoupdater_xml_content(project_id, track)
    return (content, 200) if not code else get_json_error_response(code)

@app.route('/apps/<project_id>/downloads/<file_name>', methods=['GET'])
def download_file(project_id: str, file_name: str):
    data, code = get_file_bytes(project_id, 'main', file_name)
    if not code:
        response = make_response(data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return get_json_error_response(code)

@app.route('/apps/<project_id>/<develop>/downloads/<file_name>', methods=['GET'])
def download_file_develop(project_id: str, track:str, file_name: str):
    data, code = get_file_bytes(project_id, track, file_name)
    if not code:
        response = make_response(data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return get_json_error_response(code)


if __name__ == '__main__':
    app.run(debug=True)