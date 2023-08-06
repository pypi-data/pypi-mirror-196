import warnings
from json import dumps

import click

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineCatalogue,
    parse_catalogue,
)

warnings.filterwarnings(
    "ignore",
    message="the .identification and"
    + " .serviceidentification properties will merge into .identification"
    + " being a list of properties.  This is currently implemented in"
    + " .identificationinfo.  "
    + "Please see https://github.com/geopython/OWSLib/issues/38 for more "
    + "information",
)
warnings.filterwarnings(
    "ignore",
    message="The .keywords and .keywords2 properties will merge into the"
    + " .keywords property in the future, with .keywords becoming a list of"
    + " MD_Keywords instances. This is currently implemented in .keywords2."
    + " Please see https://github.com/geopython/OWSLib/issues/301 for more "
    + "information",
)
warnings.filterwarnings(
    "ignore",
    message="The .keywords_object attribute will become .keywords proper in "
    + "the next release. .keywords_object is a list of ibstances of the "
    + "Keyword class. See for https://github.com/geopython/OWSLib/pull/765"
    + " more details.",
)


@click.group()
def command_line_interface() -> None:
    pass


@command_line_interface.command(name="describe")
@click.option(
    "--one-line",
    type=bool,
    default=False,
    help="Output JSON on one line",
)
@click.option(
    "--include-description",
    type=bool,
    default=False,
    help="Include product description in output",
)
@click.option(
    "--include-datasets",
    type=bool,
    default=False,
    help="Include product dataset details in output",
)
@click.option(
    "--include-providers",
    type=bool,
    default=False,
    help="Include product provider details in output",
)
@click.option(
    "--include-keywords",
    type=bool,
    default=False,
    help="Include product keyword details in output",
)
def describe(
    include_description: bool = False,
    include_datasets: bool = False,
    include_providers: bool = False,
    include_keywords: bool = False,
    one_line: bool = False,
) -> None:
    catalogue: CopernicusMarineCatalogue = parse_catalogue()

    def default_filter(obj):
        attributes = obj.__dict__
        if not include_description:
            attributes.pop("description", None)
        if not include_datasets:
            attributes.pop("datasets", None)
        if not include_providers:
            attributes.pop("providers", None)
        if not include_keywords:
            attributes.pop("keywords", None)
        return obj.__dict__

    json_dump = (
        dumps(catalogue, default=default_filter)
        if one_line
        else dumps(catalogue, default=default_filter, indent=2)
    )
    click.echo(json_dump)


if __name__ == "__main__":
    command_line_interface()
