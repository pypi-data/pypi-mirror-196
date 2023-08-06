import click
import urllib
import requests
import os

import loci
from loci import Project
from loci_cli.resources import SRC_README_MD


def get_server_env(server: str) -> str:
    # Chicken and egg problem here, as we only ever call this if we don't already have the ENV. Hence we
    # recreate the API call we would normally do via `loci_api_req_raw`.
    loci.cli.print_info(f"Detecting the stated environment of [bold]{server}[/bold].")
    url = urllib.parse.urljoin(server, "/api/status")

    try:
        # Show the loading animation in console
        with loci.cli.working():
            r = requests.request("GET", url, timeout=5)

        if r.ok:
            res = r.json()
            try:
                return res["env"]
            except KeyError:
                return None
    except requests.RequestException:
        raise loci.errors.LociBadServerError(server)


# Searches for a project by either name or ID, and returns the project if found, or None
def search_project_by_name_or_id(name_or_id: str) -> Project:
    try:
        # Try to turn the input into an int
        input_id = int(name_or_id)
        project = Project.get_by_id(input_id)
        return project
    except ValueError:
        # Continue on to search by string (in case the name has a number in it)
        pass

    loci.cli.print_info(f"Searching for a project using [bold]{name_or_id}[/bold]...")

    # Grab a list of all projects, see which one matches
    projects = loci.api_get_projects()

    possible_projects = []
    for project in projects:
        # Poor mans fuzzy matching
        if name_or_id in project.name:
            possible_projects.append(project)

    if len(possible_projects) > 1:
        loci.cli.print_error(f"The query [bold]{name_or_id}[/bold] matches several projects. "
                             "Be more specific.")
        return None
    elif len(possible_projects) == 0:
        loci.cli.print_warning("The query [bold]%s[/bold] did not match any projects. " % name_or_id)
        return None
    else:
        return possible_projects[0]


def login_and_get_api_key(server: str, email: str, password: str, env: str):
    loci.cli.print_info("Logging in with your credentials and obtaining an API Key."
                        f" Any previous configuration for [bold]{env}[/bold], including "
                        "server location and API keys will be invalidated.")

    # Auth via password over OAuth2.
    url = urllib.parse.urljoin(server, "/api/login")
    data = {"grant_type": "password", "username": email, "password": password}

    with loci.cli.working():
        r = requests.post(url, timeout=5, data=data)
    if r.ok:
        access_token = r.json()["access_token"]
        headers = {"Authorization": "Bearer " + access_token}
        url = urllib.parse.urljoin(server, "/api/users/me/apikey")
        with loci.cli.working():
            r = requests.post(url, timeout=5, json={}, headers=headers)

        if r.ok:
            key = r.json()["cleartext_key"]
            loci.cli.print_info(f"Saving Loci configuration for [bold]{env}[/bold].")

            # Figuring out if a default ENV has been set...
            if loci.get_local_loci_config_value("default", "env") is None:
                loci.set_local_loci_config_value("default", "env", env)
                loci.cli.print_info(f"No default environment was found, setting it to [bold]{env}[/bold].")
            else:
                default_env = loci.get_local_loci_config_value("default", "env")
                loci_config_location = loci.get_local_loci_config_location()
                loci.cli.print_warning(f"A default environment was already found, [bold]{default_env}[/bold]."
                                       f" To use the [bold]{env}[/bold] environment instead, either set the "
                                       f"default at [bold]{loci_config_location}[/bold] or set "
                                       "the [bold]LOCI_ENV[/bold] environment variable.")
            loci.set_local_loci_config_value(env, "loci_server", server)
            loci.set_local_loci_config_value(env, "api_key", key)
            loci.cli.print_success("Loci configuration saved. Test it with the [bold]loci test[/bold] command.")
        else:
            loci.cli.print_error("The API key creation has failed. This shouldn't happen, check your error logs.")
    else:
        loci.cli.print_error("The API key creation has failed. This shouldn't happen, check your error logs.")


@click.group()
def setup():
    """Server and localhost setup commands"""
    pass


@setup.command()
@click.option("-s", "--server",
              prompt="Loci Server URL",
              help="Loci Server URL, in the form https://loci-api.example.com",
              required=True,
              type=str,
              default="http://localhost:5000",
              show_default=True)
@click.option("-e", "--email",
              prompt="User Email",
              help="Email of first user, who will be an administrator.",
              required=True,
              type=str)
@click.option("-n", "--name",
              prompt="User Name",
              help="Full name of first user.",
              required=True,
              type=str)
@click.option("-p", "--password",
              prompt="User Password",
              confirmation_prompt="Confirm Password",
              help="Password of first user.",
              required=True,
              hide_input=True)
@click.option("--env",
              help="The environment of the server. Usually autodetected, but can be overridden for convenience.",
              required=False,
              type=str,
              default=None)
def server(server, email, name, password, env):
    """Sets up a new Loci Notes Server and configures the localhost"""
    loci.cli.print_info("Setting up the Loci Server at [bold]%s[/bold] with [bold]%s[/bold] as an administrator." %
                        (server, email))

    env_from_server = get_server_env(server)
    if env_from_server is None and env is None:
        loci.cli.print_error("No ENV was returned by the server. Set this manually using the [bold]--env[/bold]"
                             " option, and it's recommended to update the server to the latest release.")
        return
    if env is None and env_from_server:
        env = env_from_server
    # If env is set via command line, ignore what we got from the server
    loci.cli.print_info(f"Setting up the [bold]{env}[/bold] environment.")

    loci.cli.print_info(f"Saving server information into your preliminary local config for [bold]{env}[/bold].")
    loci.set_local_loci_config_value(env, "loci_server", server)

    loci.api_setup(env, email, name, password)
    loci.cli.print_success("The Loci server has been setup successfully.")
    login_and_get_api_key(server, email, password, env)


@setup.command()
@click.option("-s", "--server",
              prompt="Loci Server URL",
              help="Loci Server URL, in the form https://loci-api.example.com",
              required=True,
              type=str,
              default="http://localhost:5000",
              show_default=True)
@click.option("-e", "--email",
              prompt="User Email",
              help="Email of user.",
              required=True,
              type=str)
@click.option("-p", "--password",
              prompt="User Password",
              help="Password of user.",
              required=True,
              hide_input=True)
@click.option("--env",
              help="The environment of the server. Usually autodetected, but can be overridden for convenience.",
              required=False,
              type=str,
              default=None)
def localhost(server, email, password, env):
    """Sets up localhost to connect to a Loci Notes Server"""
    loci.cli.print_info("Signing in to the Loci Server at [bold]%s[/bold] with [bold]%s[/bold]." %
                        (server, email))

    env_from_server = get_server_env(server)
    if env_from_server is None and env is None:
        loci.cli.print_error("No ENV was returned by the server. Set this manually using the [bold]--env[/bold]"
                             " option, and it's recommended to update the server used to the latest release.")
        return
    if env is None and env_from_server:
        env = env_from_server
    # If env is set via command line, ignore what we got from the server
    loci.cli.print_info(f"Using the [bold]{env}[/bold] environment.")

    loci.cli.print_info(f"Saving server information into your preliminary local config for [bold]{env}[/bold].")
    loci.set_local_loci_config_value(env, "loci_server", server)
    login_and_get_api_key(server, email, password, env)


@setup.command()
@click.option("-p", "--project",
              help="Project name or ID",
              default=None,
              type=str)
def project(project: str):
    """Sets up a project in the current directory"""
    loci.cli.print_info("Setting up and/or validating the current directory for a project.")

    # This is just to help keep things straight
    project_input_str = project

    loci.cli.print_info("Checking for a project in your current directory...")
    project_from_server = loci.get_local_project(check_parents=False)

    if project_from_server is None:
        # No project exists in the current directory, make a new one.
        if project_input_str is None or project_input_str == "":
            # No name or search param was entered on the command line, ask for it directly.
            loci.cli.print_info("No project detected, enter the name or ID of the project.")
            project_input_str = click.prompt("Project name or ID", default=os.path.basename(os.getcwd()))

        project_from_server = search_project_by_name_or_id(project_input_str)
        if project_from_server is None:
            loci.cli.print_info("The project could not be found, create it?")
            create_project_input_str = click.prompt(f"Create project \"{project_input_str}\"?",
                                                    default="n",
                                                    type=click.Choice(["y", "n"], case_sensitive=False))
            if create_project_input_str.lower() == "y":
                loci.cli.print_info("Creating new project.")
                project = loci.api_new_project(project_input_str)
                loci.cli.print_success("New project [bold]%s[/bold] created successfully." % project.name)
                project_from_server = project
            else:
                # User picked "no" to creating the new project.
                loci.cli.print_info("Exiting.")
                return

        directory = os.getcwd()
        loci.set_project_config_in_local_dir(project_from_server, directory)
        loci.cli.print_info(f"Set [bold]{directory}[/bold] to use [bold]{project_from_server.name}[/bold]")

    loci.cli.print_success(f"Using [bold]{project_from_server.name}[/bold] as the Loci Notes project.")

    if not os.path.isdir("_src"):
        if os.path.isfile("_src"):
            loci.cli.print_error("A [bold]_src[/bold] was found, but it appears to be a file, not a directory. "
                                 "Rename or remove this file.")
            return
        loci.cli.print_info("The source code directory was not found, creating [bold]_src[/bold] now.")
        os.mkdir("_src")

    loci.cli.print_success("The [bold]_src[/bold] directory was found. Use this to store all source code related "
                           f"to [bold]{project_from_server.name}[/bold].")

    src_readme_path = os.path.join(os.getcwd(), "_src", "README.md")
    if not os.path.isfile(src_readme_path):
        loci.cli.print_info("Adding an informational README file to [bold]_src[/bold]...")
        with open(src_readme_path, "w") as fd:
            fd.write(SRC_README_MD)

    loci.cli.print_success(f"This directory is setup to use Loci Notes with [bold]{project_from_server.name}[/bold].")
