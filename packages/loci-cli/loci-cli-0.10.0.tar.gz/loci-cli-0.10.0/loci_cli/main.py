import click
import loci
import loci.cli

from loci_cli import PROG_NAME
from loci_cli.setup import setup
from loci_cli.user import user, list as user_list
from loci_cli.project import project
from loci_cli.project import list as project_list
from loci_cli.artifact import artifact
from loci_cli.artifact import status as artifact_status
from loci_cli.artifact import list as artifact_list
from loci_cli.note import note
from loci_cli.note import new as note_new
from loci_cli.note import list as note_list
from loci_cli.test import test
from loci_cli.config import config


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return  # pragma: nocover
    loci.cli.print_version(PROG_NAME)
    ctx.exit()


@click.group()
@click.option("-v", "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def loci_cli():
    pass


loci_cli.add_command(setup)
loci_cli.add_command(user)
loci_cli.add_command(project)
loci_cli.add_command(artifact)
loci_cli.add_command(note)
loci_cli.add_command(test)
loci_cli.add_command(config)


@click.command()
@click.pass_context
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-a", "--artifact",
              prompt="Artifact",
              help="Artifact descriptor or ID",
              required=True,
              type=str)
@click.option("-s", "--status",
              prompt=False,
              help="Artifact status update",
              type=click.Choice(["DONE", "FLAG", "TODO"], case_sensitive=False))
def status(ctx, project, artifact, status):
    """Alias for `artifact status`"""
    ctx.forward(artifact_status, project=project, artifact=artifact, status=status)


loci_cli.add_command(status)


@click.command()
@click.pass_context
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-a", "--artifact",
              prompt="Artifact",
              help="Artifact descriptor",
              required=True,
              type=str)
@click.option("-t", "--note-type",
              prompt=False,
              help="Note type",
              required=True,
              default="comment",
              show_default=True,
              type=click.Choice(["comment", "log", "snapshot_txt", "link"], case_sensitive=False))
@click.option("-T", "--tool",
              prompt=False,
              help="Tool submitting note",
              required=True,
              default="Loci CLI",
              show_default=True,
              type=str)
@click.option("-c", "--contents",
              prompt="Contents",
              help="Note contents",
              required=True,
              type=str)
def new(ctx, project: str, artifact: str, note_type: str, tool: str, contents: str):
    """Alias for `note new`"""
    ctx.forward(note_new, project=project, artifact=artifact, note_type=note_type, tool=tool, contents=contents)


loci_cli.add_command(new)


@click.command()
@click.pass_context
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-a", "--artifact",
              prompt="Artifact",
              help="Artifact descriptor or ID",
              required=True,
              type=str)
def notes(ctx, project: str, artifact: str):
    """Alias for `note list`"""
    ctx.forward(note_list, project=project, artifact=artifact)


loci_cli.add_command(notes)


@click.command()
@click.pass_context
@click.option("-f", "--filter",
              prompt=False,
              help="Filter by artifact status",
              type=click.Choice(["DONE", "FLAG", "TODO"], case_sensitive=False))
@click.option("-q", "--query",
              prompt=False,
              help="Filter by artifact content",
              type=str)
def artifacts(ctx, filter, query):
    """Alias for `artifact list`"""
    ctx.forward(artifact_list, filter=filter, query=query)


loci_cli.add_command(artifacts)


@click.command()
@click.pass_context
def projects(ctx):
    """Alias for `project list`"""
    ctx.forward(project_list)


loci_cli.add_command(projects)


@click.command()
@click.pass_context
def users(ctx):
    """Alias for `user list`"""
    ctx.forward(user_list)


loci_cli.add_command(users)


def root_entry():
    try:
        # Run environment checks on every single command. We should know the ENV of each.
        if loci.get_env() is None:
            loci_config_location = loci.get_local_loci_config_location()
            loci.cli.print_warning("Unable to detect the operating environment of this command. Unless you are "
                                   "setting up a new server, this is likely an error, and you should set "
                                   f"[bold]default.env[/bold] in [bold]{loci_config_location}[/bold], or set the "
                                   "LOCI_ENV environment variable in your system.")
        if loci.get_env() != loci.get_default_env():
            loci.cli.print_warning(f"Using non-default environment [bold]{loci.get_env()}[/bold].")
        # Print nothing for default environments

        # This sets all API calls to show the same "working" animation, so that users know something is happening.
        loci.cli.set_global_working_func()

        # Run the command.
        loci_cli()
    except loci.cli.LociError as e:
        loci.cli.print_loci_error_msg(e)


if __name__ == "__main__":
    root_entry()
