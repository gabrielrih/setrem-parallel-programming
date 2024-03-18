import click

from src.prime.parallel.manager import CompleteParallelManager, LightParallelManager
from src.prime.sequential import SequentialManager
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


@click.command()
@click.option('--mode',
              type=click.Choice(['sequential', 'parallel', 'light_parallel']),
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
@click.option('--light-way',
              type = click.BOOL,
              default = False,
              help = "When enabled the collector received just prime number")


def run(mode: str, until_number: int, batch_size: int, light_way: bool) -> None:
    if mode == 'sequential':
        SequentialManager().run(until_number)
    elif mode == 'parallel':
        CompleteParallelManager().run(until_number, batch_size)
    elif mode == 'light_parallel':
        LightParallelManager().run(until_number, batch_size)


if __name__ == '__main__':
    run()
