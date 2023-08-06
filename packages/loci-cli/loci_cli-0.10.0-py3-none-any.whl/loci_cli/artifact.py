import click
import rich
from rich.table import Table

import loci
from loci.utils import Artifact, ArtifactStatus, Project
from loci_cli.project import get_project_local_or_id


def get_artifact_by_descriptor_or_id(project: Project, descriptor_or_id: str):
    # Note that descriptor_or_id can be an int string here and still be referring to part of the descriptor,
    # not the ID.
    possible_artifact_list = []
    artifact_by_id = None
    try:
        artifact_id = int(descriptor_or_id)
        artifact = Artifact.get_by_id(artifact_id)
        if artifact is not None:
            possible_artifact_list.append(artifact)
            artifact_by_id = artifact
    except ValueError:
        # Continue on to search by string (in case the descriptor has a number in it)
        pass

    tmp_artifact_list = loci.api_get_artifacts(project, descriptor_or_id)
    for artifact in tmp_artifact_list:
        if artifact not in possible_artifact_list:
            # This ensure that if artifact ID 11 has "11" in it's descriptor, we don't add it twice.
            possible_artifact_list.append(artifact)

    if len(possible_artifact_list) > 1:
        if artifact_by_id is not None:
            # Ensure that even if we request artifact "2" where some other artifact has the number 2 in it,
            # we prioritize the artifact found by ID.
            return artifact_by_id
        loci.cli.print_error(f"The query [bold]{descriptor_or_id}[/bold] matches several artifact descriptors. "
                             "Be more specific.")
        return None
    elif len(possible_artifact_list) == 0:
        loci.cli.print_warning(f"The query [bold]{descriptor_or_id}[/bold] did not match any artifacts.")
        return None
    else:
        return possible_artifact_list[0]


def get_status_style(status: ArtifactStatus):
    if status == ArtifactStatus.TODO:
        return "[bold yellow]TODO[/bold yellow]"
    elif status == ArtifactStatus.DONE:
        return "[bold green]DONE[/bold green]"
    elif status == ArtifactStatus.FLAG:
        return "[bold red]FLAG[/bold red]"


def print_artifact_info(artifact: Artifact):
    loci.cli.print_info(f"Artifact: [{artifact.id}] '[bold]{artifact.descriptor}[/bold]' is "
                        f"{get_status_style(artifact.status)}.")


@click.group()
def artifact():
    """artifact management commands"""
    pass


@artifact.command()
@click.option("-p", "--project",
              help="Project ID, defaults to local project",
              default=None,
              type=int)
@click.option("-f", "--filter",
              prompt=False,
              help="Filter by artifact status",
              type=click.Choice(["DONE", "FLAG", "TODO"], case_sensitive=False))
@click.option("-q", "--query",
              prompt=False,
              help="Filter by artifact content",
              type=str,
              default=None)
def list(project: str, filter: str, query: str):
    """Lists all project artifacts"""
    project = get_project_local_or_id(project)
    artifact_list = loci.api_get_artifacts(project, query)

    artifact_list.sort(key=lambda x: x.id)

    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Status", style="", justify="left")
    table.add_column("Descriptor", style="", justify="left")
    table.box = rich.box.SIMPLE_HEAD

    for artifact in artifact_list:
        if filter:
            if artifact.status == ArtifactStatus(filter):
                table.add_row(str(artifact.id),
                              get_status_style(artifact.status),
                              artifact.descriptor)
        else:
            table.add_row(str(artifact.id),
                          get_status_style(artifact.status),
                          artifact.descriptor)
    loci.cli.console.print(table)


@artifact.command()
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
def status(project: str, artifact: str, status: str):
    """Shows or changes the status of an artifact"""
    project = get_project_local_or_id(project)

    artifact = get_artifact_by_descriptor_or_id(project, artifact)
    if artifact is None:
        return

    print_artifact_info(artifact)
    old_status = artifact.status

    try:
        # See if the user wants to update the status
        if not status:
            new_status = click.prompt(
                    "Set status",
                    default=artifact.status.value,
                    type=click.Choice(["DONE", "FLAG", "TODO"], case_sensitive=False))
        else:
            new_status = status

        artifact = loci.api_update_artifact_status(artifact, new_status)
        if artifact.status is not old_status:
            loci.cli.print_success("Updated artifact status.")
            print_artifact_info(artifact)
    except click.Abort:
        return
