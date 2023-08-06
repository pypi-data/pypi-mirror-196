import os
import click
import rich
from rich.table import Table

import loci
from loci import User
from loci.utils import Project


def get_project_local_or_id(project: int) -> loci.Project:
    if project is None:
        project_obj = loci.get_local_project()
        if project_obj is None:
            loci.cli.print_error("No local project could be found, and no project ID was passed in parameters. Reissue "
                                 "the command with the [bold]--project $PROJECT_ID[/bold] parameter. You can issue "
                                 "[bold]loci projects[/bold] to get a list of current projects.")
    else:
        project_obj = loci.api_get_project(project)
    if project_obj is None:
        loci.cli.print_error(f"Project [bold]{project}[/bold] could not be found. Issue "
                             "[bold]loci projects[/bold] to get a list of current projects.")
        return
    loci.cli.print_info("Project: [bold]%s[/bold]." % project_obj.name)
    return project_obj


@click.group()
def project():
    """Project management commands"""
    pass


@project.command()
def list():
    """Lists all projects"""
    projects = loci.api_get_projects()
    projects.sort(key=lambda x: x.creation_time)

    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Name", style="", justify="left")
    table.add_column("Access", style="", justify="right")
    table.box = rich.box.SIMPLE_HEAD

    for project in projects:
        table.add_row(str(project.id),
                      project.name,
                      "[green bold]\u2713[/green bold]" if project.have_access else " ")

    loci.cli.console.print(table)


@project.command()
@click.option("-n", "--name",
              prompt="Name",
              help="New project name",
              default=os.path.basename(os.getcwd()),
              required=True,
              type=str)
@click.pass_context
def new(ctx, name):
    """Creates a new project"""
    loci.cli.print_info(f"Creating new project [bold]{name}[/bold].")
    project = loci.api_new_project(name)
    loci.cli.print_success("New project created successfully.")
    loci.cli.print_info(f"Next, issue [bold]loci setup project -p {project.id}[/bold] in your project directory to "
                        f"automatically use [bold]{project.name}[/bold]. In the future, you can do all this in one "
                        "step with [bold]loci setup project[/bold].")


def get_project_by_id(ctx, param, project_id: int = None):
    if ctx.resilient_parsing:
        return

    ctx.ensure_object(dict)
    project = get_project_local_or_id(project_id)

    ctx.obj["project_id"] = project.id
    ctx.obj["project_name"] = project.name
    return project


@project.command()
@click.pass_context
# We need to reimplement the --help option here because we have to make it eager before other eager options,
# otherwise we get some weird prompts and errors when trying to get the help docs.
@click.help_option(is_eager=True)
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              prompt=False,
              required=False,
              type=int,
              callback=get_project_by_id,
              is_eager=True)
@click.option("-n", "--name",
              prompt="Project Name",
              help="Project Name",
              required=True,
              type=str,
              cls=loci.cli.default_from_context("project_name"))
def edit(ctx, project: Project, name: str):
    """Edits a project's information"""
    old_name = project.name
    if old_name == name:
        loci.cli.print_warning(f"[bold]{project.name}[/bold] was not changed.")
        return
    loci.cli.print_info("Updating project information...")
    project = loci.api_update_project(project, name)
    loci.cli.print_success(f"Project [bold]{project.name}[/bold] was updated.")


@project.command()
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
def delete(project: int):
    """Deletes a project"""
    old_project = get_project_local_or_id(project)
    loci.api_delete_project(old_project)
    loci.cli.print_success(f"[bold]{old_project.name}[/bold] deleted successfully.")


@project.command()
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
def info(project: int):
    """Shows info about a project"""
    project_obj = get_project_local_or_id(project)
    loci.cli.print_info(f"ID     : {project_obj.id}")


@project.group()
def access():
    """Project access management commands"""
    pass


@access.command("list")
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
def list_access(project: int):
    """Lists users with access to a project"""
    project = get_project_local_or_id(project)

    project_access_list = loci.api_get_project_access(project)

    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Name", style="", justify="left")
    table.add_column("Manager", style="", justify="right")
    table.box = rich.box.SIMPLE_HEAD

    for project_access_obj in project_access_list:
        user = User.get_by_id(project_access_obj.user_id)
        table.add_row(str(project_access_obj.id),
                      user.full_name,
                      "[green bold]\u2713[/green bold]" if project_access_obj.is_manager else " ")

    loci.cli.console.print(table)


@access.command()
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-u", "--user",
              prompt="User email or ID",
              help="User email or ID",
              required=True,
              type=str)
@click.option('--manager/--no-manager', default=False)
def add(project: int, user: str, manager: bool):
    """Grants a user access to a project"""
    project = get_project_local_or_id(project)

    user = loci.search_user_by_email_or_id(user)
    if user is None:
        return

    success = loci.api_add_user_project_access(project, user, manager)
    if success:
        if manager:
            loci.cli.print_success(f"[bold]{user.full_name}[/bold] was granted manager-level access "
                                   f"to [bold]{project.name}[/bold].")
            return
        else:
            loci.cli.print_success(f"[bold]{user.full_name}[/bold] was granted user-level access to "
                                   f"[bold]{project.name}[/bold].")
            return
    else:
        loci.cli.print_error(f"[bold]{user.full_name}[/bold] was not granted access.")
        return


@access.command()
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-u", "--user",
              prompt="User email or ID",
              help="User email or ID",
              required=True,
              type=str)
def remove(project: int, user: str):
    """Removes a user's project access"""
    project = get_project_local_or_id(project)

    user = loci.search_user_by_email_or_id(user)
    if user is None:
        return

    loci.api_remove_user_project_access(project, user)
