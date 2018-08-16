import os
from flask import Flask, request, jsonify
from manager import StateManager, UpdateManager
import time

app = Flask(__name__)

state = StateManager(os.environ['JSON_PATH'])
update_manger = UpdateManager(state, os.environ.get('SECOND_MASTER', 'localhost'))
update_manger.run()


@app.route('/api/resource', methods=['POST'])
def update():
    state.set_state(request.json, float(request.args.get('timestamp', time.time())))
    return jsonify({}), 200


@app.route('/api/resource', methods=['GET'])
def get():
    return jsonify(state.data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
