from flask import Flask, request, jsonify
from manager import state
import time

app = Flask(__name__)


@app.route('/api/resource', methods=['POST'])
def update():
    state.set_state(request.json, float(request.args.get('timestamp', time.time())))
    return jsonify({}), 200


@app.route('/api/resource', methods=['GET'])
def get():
    return jsonify(state.data), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)
