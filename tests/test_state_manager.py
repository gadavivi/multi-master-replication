import json
import hashlib

from fixtures import state,data,data2,timestamp


def test_set_state(state, data, data2, timestamp):
    state.set_state(data, timestamp)
    # Test set from None
    assert state.timestamp == timestamp and state.data == data, state.data_md5 == hashlib.md5(
        json.dumps(data)).hexdigest()

    # check for self.timestamp > timestamp
    state.set_state(data2, timestamp - 1)
    assert state.timestamp == timestamp and state.data == data, state.data_md5 == hashlib.md5(
        json.dumps(data)).hexdigest()

    # check for self.timestamp < timestamp
    state.set_state(data2, timestamp + 1)
    assert state.timestamp == timestamp + 1 and state.data == data2, state.data_md5 == hashlib.md5(
        json.dumps(data2)).hexdigest()


def test_set_state_tie(state, data, data2, timestamp):
    state.set_state(data2, timestamp)

    # check for self.timestamp == timestamp
    state.set_state(data, timestamp)
    assert state.timestamp == timestamp and state.data == data, state.data_md5 == hashlib.md5(
        json.dumps(data)).hexdigest()