"""Command line interface for prisma2markdown."""
import os
from pathlib import Path

import click

from .workflow import update_markdown, create_markdown


@click.group()
def prisma2mermaid():
    pass


@click.command()
@click.argument("prisma-target")
@click.option(
    "--markdown-target",
    help="Path to markdown to be updated."
    " If not set, the target will have the same name as the prisma target",
)
@click.option(
    "--force", is_flag=True, help="Set the if you wish to forced overwrite of markdown target."
)
def generate(prisma_target: os.PathLike,force: bool, markdown_target: os.PathLike = None):
    """Generate a mermaid schema from a prisma schema."""
    if markdown_target is None:
        markdown_target = Path(prisma_target).with_suffix(".md")
    create_markdown(prisma_target, markdown_target, force)


@click.command()
@click.argument("--markdown-target")
@click.option(
    "--mock",
    is_flag=True,
    help="Set this option if you wish to check output if another file first.",
)
def update(markdown_target: os.PathLike, mock):
    """Given a markdown target, update to mermaid schema with relation to its prisma schema."""
    update_markdown(markdown_target, mock)


prisma2mermaid.add_command(generate)
prisma2mermaid.add_command(update)
