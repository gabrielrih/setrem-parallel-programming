import logging

from unittest import TestCase

from src.util.logger import Logger


class TestLogger(TestCase):
    def test_get_logger(self):
        logger = Logger.get_logger(__name__)
        self.assertIsInstance(logger, logging.Logger)
