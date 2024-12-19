import os

from app.codes import (
    ERROR_FILE_EXISTS,
    ERROR_FILE_NOT_FOUND,
    ERROR_INVALID_TRACK,
    ERROR_INVALID_VERSION,
    ERROR_UNKNOWN,
    OK,
)

from app.util import compute_sha512, find_version_in_string

FILE_ROOT = os.getenv("PROJECT_ROOT")
BASE_URL = os.getenv("BASE_URL")

def create_project_branch(project_id, branch_name):
    project_folder = os.path.join(FILE_ROOT, project_id)
    try:
        branch_folder = os.path.join(project_folder, branch_name.lower())
        os.mkdir(branch_folder)
        with open(os.path.join(branch_folder, "config.toml"), "w") as file:
            file.write("")
    except Exception:
        return ERROR_UNKNOWN
    return OK

def create_project_folder(project_id):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if os.path.exists(project_folder):
        return ERROR_FILE_EXISTS
    try:
        os.mkdir(project_folder)
        main_folder = os.path.join(project_folder, "main")
        os.mkdir(main_folder)
        with open(os.path.join(main_folder, "config.toml"), "w") as file:
            file.write("")
    except Exception:
        return ERROR_UNKNOWN
    return OK

def get_project_ids():
    try:
        return os.listdir(FILE_ROOT), OK
    except Exception:
        return [], ERROR_UNKNOWN

def does_track_exist(project_id, track):
    project_folder = os.path.join(FILE_ROOT, project_id)
    return os.path.exists(os.path.join(project_folder, track))

def get_project_ids_with_track():
    try:
        projects_with_tracks = []
        for project_id in os.listdir(FILE_ROOT):
            project_path = os.path.join(FILE_ROOT, project_id)
            if os.path.isdir(project_path):
                tracks = os.listdir(project_path)
                projects_with_tracks.append([project_id, tracks])
        return projects_with_tracks, OK
    except Exception:
        return [], ERROR_UNKNOWN

def delete_project_branch(project_id, branch):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(project_folder):
        return ERROR_FILE_NOT_FOUND
    try:
        os.system(f"rmdir /s /q {os.path.join(project_folder, branch)}")
    except Exception:
        return ERROR_UNKNOWN
    return OK

def delete_project_folder(project_id):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(project_folder):
        return ERROR_FILE_NOT_FOUND
    try:
        os.system(f"rmdir /s /q {project_folder}")
    except Exception:
        return ERROR_UNKNOWN
    return OK

def upload_file_to_project(project_id, track, file_name, file_data):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(os.path.join(project_folder, track)):
        return ERROR_INVALID_TRACK
    version = find_version_in_string(file_name)
    if not version:
        return ERROR_INVALID_VERSION
    file_path = os.path.join(project_folder, track, file_name)
    with open(file_path, "wb") as file:
        file.write(file_data)
    sha512 = compute_sha512(file_path)
    with open(os.path.join(project_folder, track, "config.toml"), "w") as file:
        file.write(f'latest_file="{file_name}"\nlatest_version="{version}"\nsha512="{sha512}"')
    return OK

def get_autoupdater_xml_content(project_id, track):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(os.path.join(project_folder, track)):
        return "", ERROR_INVALID_TRACK
    with open(os.path.join(project_folder, track, "config.toml"), "r") as file:
        config = file.read()
    try:
        latest_file = config.split('latest_file="')[1].split('"')[0]
        latest_version = config.split('latest_version="')[1].split('"')[0]
        sha512 = config.split('sha512="')[1].split('"')[0]
    except Exception:
        return "", ERROR_UNKNOWN
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <item>
        <version>{latest_version}</version>
        <url>{BASE_URL}/apps/{project_id}/{track}/downloads/{latest_file}</url>
        <mandatory>false</mandatory>
        <checksum algorithm="SHA512">{sha512}</checksum>
    </item>""", OK

def get_project_config_dict(project_id, track):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(os.path.join(project_folder, track)):
        return {}, ERROR_INVALID_TRACK
    config_path = os.path.join(project_folder, track, "config.toml")
    if not os.path.exists(config_path):
        return {}, ERROR_UNKNOWN
    with open(config_path, "r") as file:
        config = file.read()
    try:
        latest_file = config.split('latest_file="')[1].split('"')[0]
        latest_version = config.split('latest_version="')[1].split('"')[0]
        sha512 = config.split('sha512="')[1].split('"')[0]
    except Exception:
        return {}, ERROR_UNKNOWN
    return {"latest_file": latest_file, "latest_version": latest_version, "sha512": sha512}, OK

def get_project_files_json(project_id, track):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(os.path.join(project_folder, track)):
        return [], ERROR_INVALID_TRACK
    try:
        files = os.listdir(os.path.join(project_folder, track))
        files.remove("config.toml")
        return [{"name": file, "size": os.path.getsize(os.path.join(project_folder, track, file))} for file in files], OK
    except Exception:
        return [], ERROR_UNKNOWN

def get_file_bytes(project_id, track, file_name):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(os.path.join(project_folder, track, file_name)):
        return None, ERROR_FILE_NOT_FOUND
    try:
        with open(os.path.join(project_folder, track, file_name), "rb") as file:
            return file.read(), OK
    except Exception:
        return None, ERROR_UNKNOWN

def delete_file_from_project(project_id, track, file_name):
    project_folder = os.path.join(FILE_ROOT, project_id)
    if not os.path.exists(os.path.join(project_folder, track, file_name)):
        return ERROR_FILE_NOT_FOUND
    try:
        os.remove(os.path.join(project_folder, track, file_name))
    except Exception:
        return ERROR_UNKNOWN
    return OK