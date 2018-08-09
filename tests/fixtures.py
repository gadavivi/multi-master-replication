import pytest
import os
from src.manager import StateManager


@pytest.fixture()
def data():
    return {'1': 'hello'}


@pytest.fixture()
def data2():
    return {'2': 'hello2'}


@pytest.fixture()
def timestamp():
    return 1533820108


@pytest.fixture()
def state(request):
    def fin():
        if os.path.exists('json.data'):
            os.remove('json.data')
    request.addfinalizer(fin)
    return StateManager('json.data')
