from src.util.decorators import timeit
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


class SequentialManager:
    @staticmethod
    def run(until_number: int) -> None:
        quantity = SequentialManager.quantity_of_prime_numbers(until_number)
        logger.info(f'There are {quantity} prime numbers before {until_number}!')

    @timeit
    @staticmethod
    def quantity_of_prime_numbers(until_number: int) -> int:
        quantity = 0
        number = 2  # starts by two because this is the first prime number
        while number <= until_number:
            prime = 1
            antecedent = 2
            while antecedent < number:
                if number % antecedent == 0:  # not prime number
                    prime = 0
                    break
                antecedent += 1
            quantity += prime
            number +=1
        return quantity
