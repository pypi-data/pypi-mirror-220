import click

from qwak_sdk.commands.models.describe._logic import execute_model_describe
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("describe", cls=QwakCommand)
@click.option("--model-id", metavar="NAME", help="Model ID")
@click.option(
    "--interface",
    metavar="",
    required=False,
    default=False,
    help="Returns the deployed build interface",
    is_flag=True,
)
@click.option(
    "--list-builds",
    metavar="",
    required=False,
    default=False,
    help="Returns the list of builds of model",
    is_flag=True,
)
def model_describe(model_id, interface, list_builds, **kwargs):
    execute_model_describe(model_id, interface, list_builds, **kwargs)
