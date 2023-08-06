import click
import rich
from rich.table import Table
import pendulum


import loci
from loci_cli.artifact import get_artifact_by_descriptor_or_id, print_artifact_info
from loci_cli.project import get_project_local_or_id


@click.group()
def note():
    """Note management commands"""
    pass


@note.command()
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-a", "--artifact",
              prompt="Artifact",
              help="Artifact descriptor or ID",
              required=True,
              type=str)
def list(project: str, artifact: str):
    """Lists all notes for an artifact"""
    project = get_project_local_or_id(project)

    artifact_obj = get_artifact_by_descriptor_or_id(project, artifact)
    if artifact_obj is None:
        return

    print_artifact_info(artifact_obj)
    notes_list = loci.api_get_notes(artifact_obj)
    notes_list.sort(key=lambda x: x.last_update_time, reverse=False)

    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Author", style="", justify="left")
    table.add_column("Updated", style="", justify="left")
    table.add_column("Tool", style="", justify="left")
    table.add_column("Type", style="", justify="left")
    table.add_column("Contents", style="", justify="left")
    table.box = rich.box.SIMPLE_HEAD

    for note in notes_list:
        natural_time = pendulum.parse(note.last_update_time).diff_for_humans()
        table.add_row(str(note.id),
                      note.user_full_name,
                      natural_time,
                      note.submission_tool,
                      note.note_type,
                      note.contents)

    loci.cli.console.print(table)


@note.command()
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
def new(project: str, artifact: str, note_type: str, contents: str, tool: str):
    """Adds a new note to a project"""
    project = get_project_local_or_id(project)
    loci.api_new_note(project, artifact, tool, note_type, contents)
    loci.cli.print_success("Note created successfully.")


def get_note_by_id(ctx, param, note_id: int):
    if not note_id or ctx.resilient_parsing:
        return

    ctx.ensure_object(dict)
    note = loci.api_get_note(note_id)

    ctx.obj["note_id"] = note.id
    ctx.obj["note_contents_old"] = note.contents
    ctx.obj["note_contents"] = note.contents
    return note.id


@note.command()
@click.pass_context
# We need to reimplement the --help option here because we have to make it eager before other eager options,
# otherwise we get some weird prompts and errors when trying to get the help docs.
@click.help_option(is_eager=True)
@click.option("-n", "--note",
              prompt="Note ID",
              help="Note ID",
              required=True,
              type=int,
              callback=get_note_by_id,
              is_eager=True)
@click.option("-c", "--contents",
              prompt="Note Contents",
              help="Note Contents",
              required=True,
              type=str,
              cls=loci.cli.default_from_context("note_contents"))
def edit(ctx, note: int, contents: str):
    """Edits an existing note"""
    if contents == ctx.obj["note_contents_old"]:
        loci.cli.print_warning(f"Note [bold]{note}[/bold] was not changed.")
        return
    loci.cli.print_info("Updating note information...")
    note = loci.api_update_note(note, contents)
    loci.cli.print_success(f"Note [bold]{note.id}[/bold] updated.")
