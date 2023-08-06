import click
import re

import loci


@click.group()
def config():
    """Localhost client configuration commands"""
    pass


@config.command()
def info():
    """Shows current client info"""
    config_file_location = loci.utils.get_local_loci_config_location()
    loci.cli.print_info(f"Getting local client configuration from [bold]{config_file_location}[/bold].")
    with open(config_file_location, "r") as fd:
        config_file_str = fd.read()
    config_file_str = re.sub(r"LOCINOTESAPI_[\w]+", "LOCINOTESAPI_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", config_file_str)
    print("#######################################################")
    print(config_file_str)
    print("#######################################################")


@config.command()
@click.option("--env",
              prompt="Environment",
              help="The environment of the config to clear.",
              required=True,
              type=str,
              default=loci.get_env())
def clear(env: str):
    """Clears out the local client configuration for an environment"""
    loci.cli.print_info(f"Clearing out local configuration for [bold]{env}[/bold]. Use [bold]loci setup "
                        "localhost[/bold] if you need to re-add this in the future for the same server.")
    loci.clear_local_loci_config(env)
