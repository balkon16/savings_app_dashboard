import json

import pytest

@pytest.fixture()
def get_test_configuration():
    with open('./tests/test_configuration.json', 'r') as f:
        conf = json.load(f)
    return conf['excel']
