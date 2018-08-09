import pytest
import requests
import mock

from fixtures import data, timestamp, state
from src.manager import UpdateManager


@pytest.fixture()
def update_manager(state):
    return UpdateManager(state, 'localhost')


@mock.patch('requests.post')
def test_update_remote_post_arrive(req_mock, update_manager, data, timestamp):
    req_mock.return_value.status_code = 200
    update_manager.local_state.set_state(data, timestamp)
    update_manager.update_remote()

    # check the regular state, when post arrives
    assert update_manager.last_timestamp == update_manager.local_state.timestamp


@mock.patch('requests.post')
def test_update_remote_nw_error(req_mock, update_manager, data, timestamp):
    req_mock.side_effect = requests.ConnectionError()
    update_manager.local_state.set_state(data, timestamp)
    with pytest.raises(requests.ConnectionError):
        update_manager.update_remote()
        assert update_manager.last_timestamp != update_manager.local_state.timestamp