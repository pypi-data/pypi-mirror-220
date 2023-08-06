import json

import pytest


class MockValue:
    """Allows any of a datatype to pass comparison within dictionary"""
    def __init__(self, name='MOCK_VALUE', data_type=None, validator=None):
        self.name = name
        self.data_type = data_type
        self.validator = validator

    def __eq__(self, item):
        if (
            (self.data_type and not isinstance(item, self.data_type)) or
            (self.validator and not self.validator(item))
        ):
            return False
        return True

    def __ne__(self, item):
        return not self.__eq__(item)

    def __repr__(self):
        return f'<ANY_{self.name}>'


@pytest.fixture(scope='session')
def any_int():
    return MockValue('INT', int)


@pytest.fixture(scope='session')
def any_str():
    return MockValue('STR', str)


@pytest.fixture(scope='session')
def any_json_str():
    return MockValue('JSON_STR', str, lambda x: json.loads(x))


@pytest.fixture(scope='session')
def two_sum_start():
    return MockValue(
        'TWO_SUM_DESCRIPTION',
        str,
        lambda x: x.startswith('Given an array of integers'),
    )


@pytest.fixture(scope='session')
def two_sum_details_json():
    with open('tests/data/two_sum_details.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session')
def two_sum_essentials():
    with open('tests/data/two_sum_essentials.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session')
def sample_two_sum_python_file():
    with open('tests/data/two_sum.py', 'r') as f:
        return f.read()