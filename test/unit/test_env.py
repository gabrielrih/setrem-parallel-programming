import src.env as envs
from unittest import TestCase


class TestEnv(TestCase):
    def test_get_env(self):
        LOG_LEVEL = envs.LOG_LEVEL
        self.assertIsInstance(LOG_LEVEL, str)
        self.assertIsNotNone(LOG_LEVEL)
