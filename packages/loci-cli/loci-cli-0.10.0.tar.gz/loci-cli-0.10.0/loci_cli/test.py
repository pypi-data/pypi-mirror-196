import click

import loci


@click.command()
def test():
    """Tests connectivity to Loci server and CLI configuration"""
    env = loci.get_env()
    if not loci.is_local_loci_setup():
        loci.cli.print_error(f"Loci CLI has not been configured for the [bold]{env}[/bold] environment. "
                             "Use the [bold]setup server[/bold] or [bold]setup localhost[/bold] command.")
        return

    loci.cli.print_info(f"Testing your local Loci configuration for [bold]{env}[/bold].")

    r = loci.loci_api_req_raw("/api/users/me", authd=True)
    if r is not None:
        loci.cli.print_success("Loci configuration is good, you are logged in as [bold]%s[/bold]." % r["full_name"])
