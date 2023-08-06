import click

from .framed import framed
from .padded import padded


CONTEXT_SETTINGS = dict(
        help_option_names = [
            '-h',
            '--help'
        ]
)

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


main.add_command(framed)
main.add_command(padded)

