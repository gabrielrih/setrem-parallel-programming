import click

from src.prime.sequential import SequentialManager
from src.prime.parallel import ParallelManager
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


@click.command()
@click.option('--mode',
              type=click.Choice(['sequential', 'parallel']),
              required=True,
              help='Mode to run')
@click.option('--until-number',
              type=click.INT,
              required=True,
              help='Until which number calculate the quantity of prime numbers')


def run(mode: str, until_number: int) -> None:
    if mode == 'sequential':
        logger.info(f'Searching quantity of prime numbers until {until_number}')
        logger.info(f'Starting in {mode =}')
        SequentialManager().run(until_number)
        return
    ParallelManager().run(until_number)


if __name__ == '__main__':
    run()
