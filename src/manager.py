import os
import json
import threading
import requests
import time
import hashlib


class StateManager(object):
    def __init__(self, path):
        self.json_path = path
        self.data, self.timestamp = self.read_json()
        self.lock = threading.Lock()
        self.data_md5 = hashlib.md5(json.dumps(self.data)).hexdigest()

    def read_json(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                data_and_time = json.load(f)
                data = data_and_time['data']
                timestamp = data_and_time['timestamp']
                return data, float(timestamp)
        return {}, None

    def write_json(self, data, timestamp):
        with open(self.json_path, 'w') as outfile:
            json.dump({'data': data, 'timestamp': timestamp}, outfile)

    def set_state(self, data, timestamp):
        data_md5 = hashlib.md5(json.dumps(self.data)).hexdigest()
        with self.lock:
            # If the timestamps are equal break the tie by taking the one with the smaller lexicography order.
            if self.timestamp is None or self.timestamp < timestamp or \
                    (self.timestamp == timestamp and data_md5 < self.data_md5):
                self.timestamp = timestamp
                self.data = data
                self.write_json(data, timestamp)
                self.data_md5 = data_md5


class UpdateManager(object):
    def __init__(self, local_state, second_master):
        self.last_timestamp = None
        self.data_md5 = None
        self.second_master = second_master
        self.local_state = local_state

    def update_remote(self):
        ###   there are 3 option   ###
        # 1. In a regular case when a post has arrived, The service is trying to update the other master with his value.
        # 2. One or two server got back up after an error, in this case because it is persistent
        #   (local_state.timestamp != last_timestamp), So each master will try to update the other with his value.
        #    and the one with the earlier timestamp will get the update.
        # 3. There is a network error, it means that r.status_code != 200 so the live master will keep trying to update
        #    The other master.
        if self.local_state.timestamp != self.last_timestamp or self.data_md5 != self.local_state.data_md5:
            r = requests.post('http://%s/api/resource?timestamp=%s' % (self.second_master,
                                                                       repr(self.local_state.timestamp)),
                              json=json.dumps(self.local_state.data))
            if r.status_code == 200:
                self.last_timestamp = self.local_state.timestamp
                self.data_md5 = self.local_state.data_md5

    def update_remote_loop(self, sleep):
        while True:
            try:
                self.update_remote()
            except requests.ConnectionError:
                pass
            time.sleep(sleep)

    def run(self, sleep=1):
        thread = threading.Thread(target=self.update_remote_loop, args=(sleep,))
        thread.start()

