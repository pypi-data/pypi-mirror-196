from typing import List

from loci import Project, User, ProjectAccess, Artifact, loci_api_req_raw
from loci.utils import ArtifactStatus, Note


# We need to pass ENV here because the default is not set and the full config isn't present before server setup, only
# after.
def api_setup(env: str, email: str, name: str, password: str):
    data = {"email": email, "full_name": name, "password": password}
    return loci_api_req_raw("/api/setup", method="POST", data=data, env=env)


def api_get_project(id: int) -> Project:
    project = Project.get_by_id(id)
    return project


def api_get_projects() -> List[Project]:
    r = loci_api_req_raw("/api/projects", authd=True)
    projects = []
    if r is not None:
        for project_dict in r:
            projects.append(Project.from_dict(project_dict))
    return projects


def api_new_project(name: str) -> Project:
    r = loci_api_req_raw("/api/projects", method="POST", data={"name": name}, authd=True)
    return Project.from_dict(r)


def api_update_project(project: Project, new_name: str) -> Project:
    project_updates = {}
    project_updates["name"] = new_name

    r = loci_api_req_raw(f"/api/projects/{project.id}",
                         method="PUT",
                         data=project_updates,
                         authd=True)
    return Project.from_dict(r)


def api_delete_project(project: Project) -> bool:
    loci_api_req_raw(f"/api/projects/{project.id}", method="DELETE", authd=True)
    return True


def api_get_me() -> User:
    r = loci_api_req_raw("/api/users/me", authd=True)
    return User.from_dict(r)


def api_get_users() -> List[User]:
    r = loci_api_req_raw("/api/users", authd=True)
    users = []
    if r is not None:
        for user_dict in r:
            users.append(User.from_dict(user_dict))
    return users


def api_new_user(email: str, full_name: str, password: str) -> User:
    r = loci_api_req_raw("/api/users", method="POST",
                         data={"email": email, "full_name": full_name, "password": password},
                         authd=True)
    return User.from_dict(r)


def api_delete_user(user: User) -> bool:
    loci_api_req_raw(f"/api/users/{user.id}", method="DELETE", authd=True)
    return True


def api_update_user(user: User, new_full_name: str = None, new_password: str = None) -> User:
    user_updates = {}
    if new_full_name:
        user_updates["full_name"] = new_full_name
    if new_password:
        user_updates["password"] = new_password

    r = loci_api_req_raw(f"/api/users/{user.id}", method="PUT", data=user_updates, authd=True)
    return User.from_dict(r)


# Searches for a user by either name or ID, and returns the user if found, or None
def search_user_by_email_or_id(email_or_id: str) -> User:
    try:
        # Try to turn the input into an int
        input_id = int(email_or_id)
        user = User.get_by_id(input_id)
        return user
    except ValueError:
        # Continue on to search by string (in case the name has a number in it)
        pass

    # Grab a list of all users, see which one matches
    users = api_get_users()

    for user in users:
        if email_or_id == user.email:
            return user
    return None


def api_get_project_access(project: Project) -> List[ProjectAccess]:
    r = loci_api_req_raw(f"/api/project/{project.id}/access", authd=True)
    project_access_list = []
    if r is not None:
        for project_access_dict in r:
            project_access_list.append(ProjectAccess.from_dict(project_access_dict))
    return project_access_list


def api_add_user_project_access(project: Project, user: User, manager: bool = False) -> bool:
    body = {
        "user_id": user.id,
        "is_manager": manager
    }
    r = loci_api_req_raw(f"/api/projects/{project.id}/access",
                         method="POST",
                         data=body,
                         authd=True)
    if r is not None:
        return True
    return False


def api_remove_user_project_access(project: Project, user: User) -> bool:
    # Get the project access list
    project_access_list = api_get_project_access(project)

    access_id = None
    for access in project_access_list:
        if access.user_id == user.id:
            access_id = access.id
            break
    if access_id:
        loci_api_req_raw(f"/api/project_access/{access_id}", method="DELETE", authd=True)
        return True
    else:
        # User probably doesn't actually have access.
        return False


def api_get_artifacts(project: Project, query: str = None) -> List[Artifact]:
    url_path = f"api/projects/{project.id}/artifacts"
    if query:
        r = loci_api_req_raw(url_path, params={"q": query}, authd=True)
    else:
        r = loci_api_req_raw(url_path, authd=True)

    artifacts = []
    for artifact_dict in r:
        tmp_obj = Artifact.from_dict(artifact_dict)
        artifacts.append(tmp_obj)
    return artifacts


def api_update_artifact_status(artifact: Artifact, status: ArtifactStatus) -> Artifact:
    if not status == artifact.status:
        artifact_updates = {}
        artifact_updates["status"] = status.upper()

        r = loci_api_req_raw(f"/api/artifacts/{artifact.id}", method="PUT", data=artifact_updates, authd=True)
        return Artifact.from_dict(r)
    else:
        # Do nothing, status is already correct.
        return artifact


def api_get_notes(artifact: Artifact) -> List[Note]:
    r = loci_api_req_raw(f"/api/artifacts/{artifact.id}/notes", authd=True)
    notes = []
    for note_dict in r:
        tmp_obj = Note.from_dict(note_dict)
        notes.append(tmp_obj)
    return notes


def api_new_note(project: Project,
                 artifact_descriptor: str,
                 submission_tool: str,
                 note_type: str,
                 contents: str) -> Note:
    new_note = {}
    new_note["artifact_descriptor"] = artifact_descriptor
    new_note["submission_tool"] = submission_tool
    new_note["note_type"] = note_type.upper()
    new_note["contents"] = contents

    r = loci_api_req_raw(f"/api/projects/{project.id}/notes", method="POST", data=new_note, authd=True)
    return Note.from_dict(r)


def api_get_note(id: int) -> Note:
    r = loci_api_req_raw(f"/api/notes/{id}", authd=True)
    return Note.from_dict(r)


def api_update_note(note_id: int, new_contents: str) -> Note:
    note_update = {}
    note_update["contents"] = new_contents
    r = loci_api_req_raw(f"/api/notes/{note_id}", method="PUT", data=note_update, authd=True)
    return Note.from_dict(r)
