import subprocess
import sys

from pathlib import Path

import click


def run(args):
    command = [f'{Path(__file__).parent}/docker-compose'] + list(args)
    result = subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)


@click.command('docker-compose')
@click.argument('args', nargs=-1)
def docker_compose(args):
    run(args)


if __name__ == '__main__':
    docker_compose()
