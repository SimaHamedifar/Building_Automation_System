"""
Simple software BACnet 'MS/TP' simulator.
It exposes REST endpoints to GET/PUT "object" values and simulates device behavior.
This is not real BACnet protocol; it's a software stand-in so you can build controller logic without hardware.
To move to real BACnet, replace this with BACpypes based stack or a BACnet gateway.
"""

from flask import Flask, jsonify, request
from threading import Thread
import time
import datetime

app = Flask(__name__)

# simple in-memory DB for devices
devices = {
    1001: {  # device id
        'device_id': 1001,
        'name': 'Simulated MSTP Thermostat Zone 1',
        'objects': {
            'presentValue_temperature': 22.0,
            'presentValue_humidity': 40.0,
            'presentValue_heating_setpoint': 20.0,
            'presentValue_cooling_setpoint': 26.0,
            'presentValue_mode': 'auto',  # auto/heat/cool/off
        }
    }
}

@app.route('/devices', methods=['GET'])
def list_devices():
    return jsonify(list(devices.values()))

@app.route('/devices/<int:device_id>/objects', methods=['GET'])
def list_objects(device_id):
    dev = devices.get(device_id)
    if not dev:
        return jsonify({'error':'device not found'}), 404
    return jsonify(dev['objects'])

@app.route('/devices/<int:device_id>/objects/<string:obj>', methods=['GET', 'PUT'])
def get_set_object(device_id, obj):
    dev = devices.get(device_id)
    if not dev:
        return jsonify({'error':'device not found'}), 404
    if request.method == 'GET':
        val = dev['objects'].get(obj)
        return jsonify({'value': val})
    else:
        body = request.json
        if 'value' not in body:
            return jsonify({'error':'value required'}), 400
        dev['objects'][obj] = body['value']
        return jsonify({'ok': True, 'value': body['value']})

def run_server():
    app.run(port=5005, debug=False)

if __name__ == "__main__":
    print("Starting BACnet MS/TP simulator (HTTP shim) on port 5005")
    run_server()
