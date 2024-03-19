from enum import Enum

from src.util.converters import StringConverter


class Rank(Enum):
    EMITTER = 0
    COLLECTOR = 1


class Signals(Enum):
    END_SIGNAL = 'end_signal'


class IsPrimeSerializer:
    DELIMITER = ':'

    @staticmethod
    def serialize(number: str, is_prime: bool) -> str:
        data = f'{number}{IsPrimeSerializer.DELIMITER}{is_prime}'
        return str(data)

    @staticmethod
    def deserialize(data: str):
        raw_data = data.split(IsPrimeSerializer.DELIMITER)
        number = int(raw_data[0])
        is_prime = StringConverter.string_to_bool(raw_data[1])
        return number, is_prime


class NumbersSerializer:
    DELIMITER = ':'

    @staticmethod
    def serialize(from_number: int, to_number: int) -> str:
        data = f'{from_number}{NumbersSerializer.DELIMITER}{to_number}'
        return str(data)

    @staticmethod
    def deserialize(data: str):
        raw_data = data.split(NumbersSerializer.DELIMITER)
        from_number = int(raw_data[0])
        to_number = int(raw_data[1])
        return from_number, to_number
