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
@click.option('--batch-size',
              type=click.INT,
              default=50,
              required=False,
              help='Batch size to reduce communication overhead (just on parallel mode)')


def run(mode: str, until_number: int, batch_size: int) -> None:
    if mode == 'sequential':
        SequentialManager().run(until_number)
        return
    ParallelManager().run(until_number, batch_size)


if __name__ == '__main__':
    run()
