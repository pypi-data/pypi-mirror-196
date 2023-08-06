# site
import click
from importlib.metadata import version as dist_version, files as dist_files

# package
from .paramtypes import DemoIdType
from .util import (
    collect_demos,
    demo_requirements_satisfied,
    YELLOW,
    ANSI_RESET,
)
from ..__version__ import __version__


def get_dist_path(distribution_name):
    # HACK: potential to break if volux packages contains multiple __init__.py files?
    return (
        [p for p in dist_files(distribution_name) if "__init__.py" in str(p)][0]
        .locate()
        .joinpath("..")
        .resolve()
    )


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option(
    "-l",
    "--list",
    "list_",
    type=click.Choice(["demos"]),
    help="List available demos.",
)
@click.version_option(
    None,
    "--version",
    "-V",
    message=f"%(package)s {__version__} from {__file__}\n  volux {dist_version('volux')} from {get_dist_path('volux')}",
)
@click.pass_context
def cli(ctx, verbose, list_):
    """A simple general-purpose program for Volux."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj["VERBOSE"] = verbose

    if ctx.invoked_subcommand is None:
        if list_ == "demos":
            _list_demos()
        else:
            with click.Context(cli) as ctx:
                click.echo(cli.get_help(ctx))


@cli.command()
@click.argument("name", type=DemoIdType())
@click.pass_context
def demo(ctx, name):
    """Run specified demo."""
    demos = collect_demos()
    demo_dict = {demo["id"]: demo["demo"] for demo in demos}

    if name in demo_dict:
        _demo = demo_dict[name]
        if demo_requirements_satisfied(_demo):
            _demo().main()
        else:
            exit(1)
        return

    else:
        _list_demos()
        click.echo()
        click.echo(f"Error: No such demo: {name}")
        click.echo(
            f"{YELLOW}Tip: See 'volux --list demos' for a list of available demos.{ANSI_RESET}"
        )


def _list_demos():
    # get list of demos
    demos = collect_demos()

    # get length of longest demo name
    longest_demo_name_char_count = 0
    for id in (len(demo["id"]) for demo in demos):
        if id > longest_demo_name_char_count:
            longest_demo_name_char_count = id

    click.echo("Available demos:")

    for demo in demos:
        click.echo(
            f"  {demo['id']:<{longest_demo_name_char_count}}  {demo['description']}"
        )
