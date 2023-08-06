import click
import rich
from rich.console import Console

from loci import WORKING_FUNC
from loci.errors import LociError
from loci.utils import loci_api_req_raw
from ..__version__ import __version__

console = Console()


def _print_line(header, msg):
    rich.print(header, msg)


def print_info(msg):
    _print_line("[[bold blue]INFO[/bold blue]]", msg)


def print_success(msg):
    _print_line("[[bold green]SUCCESS[/bold green]]", msg)


def print_warning(msg):
    _print_line("[[bold yellow]WARNING[/bold yellow]]", msg)


def print_error(msg, fatal=True):
    _print_line("[[bold red]ERROR[/bold red]]", msg)

    if fatal:
        quit(-1)


def print_version(prog_name):
    rich.print("[bold]%s[/bold] v%s" % (prog_name, __version__))


def working():
    return console.status("Working...")


def print_loci_error_msg(exception: LociError, fatal: bool = True):
    if not isinstance(exception, LociError):
        print_error("A non-Loci note error was passed to handle_loci_error. This should not happen.", fatal=True)
        return
    print_error(exception.default_msg, fatal=fatal)


def set_global_working_func():
    global WORKING_FUNC
    WORKING_FUNC=working


# From https://stackoverflow.com/a/56043912
def default_from_context(default_name):
    class OptionDefaultFromContext(click.Option):
        def get_default(self, ctx, call: bool = True):
            if ctx.obj is None:
                return None 
            self.default = ctx.obj[default_name]
            return super(OptionDefaultFromContext, self).get_default(ctx, call=call)

    return OptionDefaultFromContext
