import unittest
from unittest.mock import patch
import json
from sahayak.raahiAI.raahi import get_train_info


def get_mock_raahi_response(*args, **kwargs):
    with open('sample_raahi_output.json') as f:
        return json.load(f)


class TestRaahi(unittest.TestCase):
    def test_get_train_info(self):
        pass


if __name__ == "__main__":
    unittest.main()
