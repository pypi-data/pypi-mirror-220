"""
Entry point for CLI. Define and parse CLI arguments.
"""
from pathlib import Path

import click

from localeet.get_leetcode_problem import run

DIFFICULTY_MAP = {
    'easy': 1,
    'medium': 2,
    'hard': 3,
    '1': 1,
    '2': 2,
    '3': 3,
}


@click.command()
@click.option(
    '--max_difficulty', '--max',
    help='Max difficulty allowed',
    type=click.Choice(list(DIFFICULTY_MAP.keys())),
)
@click.option(
    '--min_difficulty', '--min',
    help='Min difficulty allowed',
    type=click.Choice(list(DIFFICULTY_MAP.keys())),
)
@click.option(
    '--output_path', '--path', '-o',
    help='Output path for code file created. Default is cwd. '
         'Will create new directories as needed',
    default='.',
)
def main(max_difficulty: str, min_difficulty: str, output_path: str) -> None:
    """Entry point for CLI. Parse CLI arguments."""
    max_difficulty = DIFFICULTY_MAP.get(max_difficulty, 3)
    min_difficulty = DIFFICULTY_MAP.get(min_difficulty, 1)
    output_path = Path(output_path)

    run(max_difficulty, min_difficulty, output_path)
