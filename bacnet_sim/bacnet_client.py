# bacnet_sim/bacnet_client.py
import requests
import time

BASE = "http://localhost:5005"

def read_object(device_id, obj):
    r = requests.get(f"{BASE}/devices/{device_id}/objects/{obj}")
    r.raise_for_status()
    return r.json()['value']

def write_object(device_id, obj, value):
    r = requests.put(f"{BASE}/devices/{device_id}/objects/{obj}", json={'value': value})
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    device = 1001
    print("Initial objects:", requests.get(f"{BASE}/devices/{device}/objects").json())
    print("Reading temp:", read_object(device, 'presentValue_temperature'))
    print("Setting heating setpoint to 19.5")
    write_object(device, 'presentValue_heating_setpoint', 19.5)
    print("New heating setpoint:", read_object(device, 'presentValue_heating_setpoint'))
