import os
import pathlib
import configparser
import requests
from enum import Enum, auto
import urllib

from loci import LOCI_CONFIG_DIR, LOCI_CONFIG_FILENAME, LOCI_PROJECT_FILENAME, WORKING_FUNC
from loci.errors import (
    LociClientError,
    LociLocalConfigReadError,
    LociLocalProjectNotFoundError,
    LociNoEnvError,
    LociNoServerError,
    LociBadServerError,
    LociNoApiKeyError,
    LociServerInputError,
    LociServerAuthenticationError,
    LociServerAuthorizationError,
    LociServerObjectNotFoundError,
    LociServerUnknownError,
)


class User():
    id: int
    full_name: str
    email: str
    is_active: bool

    def __init__(self, id: int, full_name: str, email: str, is_active: bool):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.is_active = is_active

    @staticmethod
    def from_dict(r: dict) -> "User":
        return User(r["id"],
                    r["full_name"],
                    r["email"],
                    r["is_active"])

    @staticmethod
    def get_by_id(id: int) -> "User":
        r = loci_api_req_raw(f"/api/users/{id}", method="GET", authd=True)
        if r is not None:
            return User.from_dict(r)
        return None


class Project():
    id: int
    name: str
    creation_time: str
    have_access: bool

    def __init__(self, id: int, name: str, creation_time: str, have_access: bool):
        self.id = id
        self.name = name
        self.creation_time = creation_time
        self.have_access = have_access

    @staticmethod
    def from_dict(r: dict) -> "Project":
        try:
            have_access = r["have_access"]
        except KeyError:
            have_access = True

        return Project(r["id"],
                       r["name"],
                       r["creation_time"],
                       # This is terrible, fix once https://gitlab.com/loci-notes/loci-server/-/issues/90
                       # is implemented.
                       have_access)

    @staticmethod
    def get_by_id(id: int) -> "Project":
        r = loci_api_req_raw(f"/api/projects/{id}", method="GET", authd=True)
        if r is not None:
            tmp_project = Project(r["id"],
                                  r["name"],
                                  r["creation_time"],
                                  # This is terrible, fix once https://gitlab.com/loci-notes/loci-server/-/issues/90
                                  # is implemented.
                                  True)
            return tmp_project
        return None


class ProjectAccess():
    id: int
    project_id: int
    user_id: int
    is_manager: bool

    def __init__(self, id: int, project_id: int, user_id: int, is_manager: bool):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.is_manager = is_manager

    @staticmethod
    def from_dict(r: dict) -> "ProjectAccess":
        return ProjectAccess(r["id"],
                             r["project_id"],
                             r["user_id"],
                             r["is_manager"])

    @staticmethod
    def get_by_id(id: int) -> "ProjectAccess":
        r = loci_api_req_raw(f"/api/project_access/{id}", method="GET", authd=True)
        if r is not None:
            return ProjectAccess(r["id"],
                                 r["project_id"],
                                 r["user_id"],
                                 r["is_manager"])
        return None


# From https://docs.python.org/3/howto/enum.html#using-automatic-values
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class ArtifactStatus(AutoName):
    TODO = auto()
    DONE = auto()
    FLAG = auto()


class Artifact():
    id: int
    descriptor: str
    project_id: Project
    status: ArtifactStatus

    def __init__(self, id: int, descriptor: str, project_id: int, status: ArtifactStatus):
        self.id = id
        self.descriptor = descriptor
        self.project_id = project_id
        self.status = status

    @staticmethod
    def from_dict(r: dict) -> "Artifact":
        return Artifact(r["id"],
                        r["descriptor"],
                        r["project_id"],
                        ArtifactStatus(r["status"]))

    @staticmethod
    def get_by_id(id: int) -> "Artifact":
        r = loci_api_req_raw(f"/api/artifacts/{id}", method="GET", authd=True)
        if r is not None:
            return Artifact.from_dict(r)
        return None


class Note():
    id: int
    artifact_id: int
    submission_tool: str
    note_type: str
    contents: str
    last_update_time: str
    user_id: int
    user_full_name: str

    def __init__(self,
                 id: int,
                 artifact_id: int,
                 submission_tool: str,
                 note_type: str,
                 contents: str,
                 last_update_time: str,
                 user_id: int,
                 user_full_name: str):
        self.id = id
        self.artifact_id = artifact_id
        self.submission_tool = submission_tool
        self.note_type = note_type
        self.contents = contents
        self.last_update_time = last_update_time
        self.user_id = user_id
        self.user_full_name = user_full_name

    @staticmethod
    def from_dict(r: dict) -> "Note":
        try:
            if r["update_time"] is None or r["update_time"] == "":
                raise KeyError
            return Note(r["id"],
                        r["artifact_id"],
                        r["submission_tool"],
                        r["note_type"],
                        r["contents"],
                        r["update_time"],
                        r["user"]["id"],
                        r["user"]["full_name"])
        except KeyError:
            # This is fine, the update time is optional from the server.
            return Note(r["id"],
                        r["artifact_id"],
                        r["submission_tool"],
                        r["note_type"],
                        r["contents"],
                        r["creation_time"],
                        r["user"]["id"],
                        r["user"]["full_name"])

    @staticmethod
    def get_by_id(id: int) -> "Note":
        r = loci_api_req_raw(f"/api/notes/{id}", method="GET", authd=True)
        if r is not None:
            return Note.from_dict(r)
        return None


def get_default_env():
    if get_local_loci_config_value("default", "env") is not None:
        env = get_local_loci_config_value("default", "env")
    else:
        env = None
    return env


def get_env():
    # First look for a project file, and use that ENV if it exists
    if get_project_config_value_from_local_dir("env") is not None:
        env = get_project_config_value_from_local_dir("env")
    # If it doesn't exist, use the LOCI_ENV environment variable.
    elif os.environ.get("LOCI_ENV") is not None:
        env = os.environ["LOCI_ENV"]
    elif get_default_env() is not None:
        env = get_default_env()
    else:
        env = None
    return env


# This function from https://github.com/tensorflow/tensorboard/blob/master/tensorboard/uploader/util.py
# Apache 2 licensed
def get_local_user_config_directory():
    """Returns a platform-specific root directory for user config settings."""
    # On Windows, prefer %LOCALAPPDATA%, then %APPDATA%, since we can expect the
    # AppData directories to be ACLed to be visible only to the user and admin
    # users (https://stackoverflow.com/a/7617601/1179226). If neither is set,
    # return None instead of falling back to something that may be world-readable.
    if os.name == "nt":
        appdata = os.getenv("LOCALAPPDATA")
        if appdata:
            return appdata
        appdata = os.getenv("APPDATA")
        if appdata:
            return appdata
        return None
    # On non-windows, use XDG_CONFIG_HOME if set, else default to ~/.config.
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        return xdg_config_home
    return os.path.join(os.path.expanduser("~"), ".config")


def get_local_loci_dir() -> str:
    loci_dir = pathlib.Path(get_local_user_config_directory(), LOCI_CONFIG_DIR)
    # Create the directory if it doesn't exist yet.
    loci_dir.mkdir(parents=True, exist_ok=True)
    return str(loci_dir)


def get_local_loci_config_location() -> str:
    return str(pathlib.Path(get_local_loci_dir(), LOCI_CONFIG_FILENAME))


def get_local_loci_config():
    try:
        config = configparser.ConfigParser()
        config.sections()
        config.read(get_local_loci_config_location())
        return config
    except configparser.Error:
        raise LociLocalConfigReadError(get_local_loci_config_location())


def is_local_loci_setup() -> bool:
    try:
        config = get_local_loci_config()
        env = get_env()
        if config[env]["api_key"] is not None and config[env]["loci_server"] is not None:
            return True
        return False
    except LociClientError:
        # This is fine, it just means that we haven't ever setup Loci on this host.
        return False
    except KeyError:
        return False


def set_local_loci_config_value(env: str, key: str, value: str):
    try:
        config = get_local_loci_config()
    except LociLocalConfigReadError:
        # This is fine, it just means that we haven't ever setup Loci on this host.
        pass

    if env not in config:
        config[env] = {}
    config[env][key] = value

    with open(get_local_loci_config_location(), "w") as configfile:
        config.write(configfile)


def get_local_loci_config_value(env: str, key: str):
    config = get_local_loci_config()
    if env not in config:
        return None
    if key not in config[env]:
        return None
    return config[env][key]


def clear_local_loci_config(env: str) -> bool:
    try:
        config = get_local_loci_config()
    except LociLocalConfigReadError:
        # This is fine, it just means that we haven't ever setup Loci on this host.
        return True

    if env not in config:
        return True
    config.pop(env)

    with open(get_local_loci_config_location(), "w") as configfile:
        config.write(configfile)
    return True


def set_project_config_in_local_dir(project: Project, fq_directory: str):
    config = configparser.ConfigParser()
    config.sections()
    config["default"] = {}
    config["default"]["env"] = get_env()
    config["default"]["project_id"] = str(project.id)

    with open(pathlib.Path(fq_directory, LOCI_PROJECT_FILENAME), "w") as configfile:
        config.write(configfile)


# This will get the project information from a given directory. If `check_parents` is False, it will
# NOT recurse up through directories until a project file is found or a top level directory is hit.
# Set this to false if you want to check ONLY the current directory for a project.
def get_project_config_value_from_local_dir(key: str, fq_directory=None, check_parents: bool = True) -> str:
    config = configparser.ConfigParser()
    config.sections()

    if fq_directory is None:
        # If no dir is passed, used the users current directory.
        fq_directory = os.getcwd()

    current_dir = fq_directory
    last_dir = ""

    while True:
        try:
            config.read(pathlib.Path(fq_directory, LOCI_PROJECT_FILENAME))
            return config["default"][key]
        except KeyError:
            if not check_parents:
                # Do NOT recurse up through directories.
                return None
            if current_dir == pathlib.Path.home() or current_dir == last_dir:
                return None
            # Recurse up one directory
            last_dir = current_dir
            current_dir = os.path.dirname(current_dir)


def get_local_project(fq_directory=None, check_parents: bool = True) -> Project:
    """Gets the project from the current directory.

    Search current directory for the local project info, look it up to ensure it's valid, and return the project.
    If found, the project name will be printed. If it's not found, an error will be printed, and then the program
    will exit with a non-zero value.

    Parameters:

    Returns:
    Project: Loci Project or None
    """
    project_id = get_project_config_value_from_local_dir("project_id",
                                                         fq_directory=fq_directory,
                                                         check_parents=check_parents)
    if project_id is None:
        return None
    project = Project.get_by_id(int(project_id))

    if project is None:
        raise LociLocalProjectNotFoundError()
    return project


def loci_api_req_raw(api_url: str,
                     env: str = None,
                     method: str = "GET",
                     authd: bool = False,
                     data: dict = {},
                     params: dict = {}):
    if env is None:
        env = get_env()
        if env is None:
            # We have no ENV to know where to pull the server information from.
            raise LociNoEnvError()

    # Lookup the server for ENV
    server = get_local_loci_config_value(env, "loci_server")
    if server is None:
        raise LociNoServerError(env)

    # Build the full API URL with the server.
    url = urllib.parse.urljoin(server, api_url)

    headers = {}
    if authd:
        # This call needs authentication
        # Pull the API key from the global Loci config based on the ENV
        api_key = get_local_loci_config_value(env, "api_key")
        if api_key is None:
            raise LociNoApiKeyError()
        headers["X-API-KEY"] = api_key

    try:
        if WORKING_FUNC:
            # Show the loading animation in console
            with WORKING_FUNC():
                r = requests.request(method, url, headers=headers, timeout=5, json=data, params=params)
        else:
            # Dont' show a loading animation, just wait until the call returns.
            r = requests.request(method, url, headers=headers, timeout=5, json=data, params=params)

        if r.ok:
            if len(r.text) == 0:
                # Handles cases where there's a 204 or something with non content, but success.
                return {}
            res = r.json()
            return res
        elif r.status_code == 400:
            # This is similar to a 422, but we generate this, not FastAPI.
            raise LociServerInputError(r.json()["detail"])
        elif r.status_code == 401:
            raise LociServerAuthenticationError(r.json()["detail"])
        elif r.status_code == 403:
            raise LociServerAuthorizationError(r.json()["detail"])
        elif r.status_code == 404:
            raise LociServerObjectNotFoundError(r.json()["detail"])
        elif r.status_code == 422:
            # The reason we don't give details here is that a 422 is normally automatically generated by the server,
            # not something we can control and to which we can add details.
            raise LociServerInputError()

        else:
            try:
                detail = r.json()["detail"]
                raise LociServerUnknownError(code=r.status_code, detail_msg=detail)
            except KeyError:
                raise LociServerUnknownError(code=r.status_code)
    except requests.RequestException:
        raise LociBadServerError(server)
