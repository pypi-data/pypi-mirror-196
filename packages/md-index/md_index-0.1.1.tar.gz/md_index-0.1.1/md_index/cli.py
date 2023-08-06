from pathlib import Path

import click

from md_index.index import generate_index


@click.command()
@click.option(
    "-i",
    "--input-dir",
    type=click.Path(exists=True),
    default=".",
    help="Input directory.",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False, writable=True),
    default="docs",
    help="Output directory.",
)
@click.option(
    "-d",
    "--depth",
    type=click.INT,
    default=1,
    help="Depth of the file tree to generate, 1 or 2.",
)
@click.option(
    "-u",
    "--url-prefix",
    type=click.STRING,
    default="",
    help="Prefix for the URLs in the generated index.",
)
def generate(input_dir: str, output_dir: str, depth: int, url_prefix: str):
    generate_index(Path(input_dir), Path(output_dir), depth, url_prefix)
    click.echo(f'Markdown index generated for "{input_dir}"" in "{output_dir}"')


if __name__ == "__main__":
    generate()
