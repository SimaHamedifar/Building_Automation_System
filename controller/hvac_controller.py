# controller/hvac_controller.py
"""
Simple BMS controller loop:
- Reads latest zone temperature from DB
- Computes heating/cooling setpoints based on schedule and outdoor temp
- Writes setpoints to simulated BACnet device
- Stores setpoints to the DB
"""

import time
import requests
import sqlalchemy
import pandas as pd
from datetime import datetime
import os

DB_URL = os.getenv("BMS_DB_URL", "postgresql+psycopg2://bms:bms_pass@localhost:5432/bms_db")
BACNET_BASE = os.getenv("BACNET_SIM_BASE", "http://localhost:5005")
DEVICE_ID = 1001
ZONE_NAME = "Zone 1"

engine = sqlalchemy.create_engine(DB_URL)

def get_latest_zone_temp(zone_name=ZONE_NAME):
    q = "SELECT ts, zone_air_temp FROM energyplus_timeseries WHERE zone_name=%s ORDER BY ts DESC LIMIT 1"
    with engine.begin() as conn:
        rows = conn.execute(sqlalchemy.text(q), (zone_name,)).fetchall()
        if not rows:
            return None
        return rows[0][1]

def compute_setpoints(current_temp, outdoor_temp=None):
    # Very simple rule:
    # target comfortable range: 21-24 C
    if current_temp is None:
        return 21.0, 24.0
    if current_temp < 20:
        # colder than desired: raise heating setpoint
        return 22.0, 24.0
    elif current_temp > 25:
        # hotter than desired: lower cooling setpoint
        return 21.0, 23.0
    else:
        return 21.5, 23.5

def write_setpoint_to_bacnet(device_id, obj, value):
    r = requests.put(f"{BACNET_BASE}/devices/{device_id}/objects/{obj}", json={'value': value})
    return r.ok

def save_setpoint_to_db(zone_name, heating_sp, cooling_sp):
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text(
            "INSERT INTO setpoints (ts, zone_name, heating_setpoint, cooling_setpoint) VALUES (:ts, :zn, :h, :c)"),
            {"ts": datetime.utcnow(), "zn": zone_name, "h": heating_sp, "c": cooling_sp}
        )

def controller_loop(poll_interval=15):
    print("Starting HVAC controller loop (press Ctrl+C to stop)")
    while True:
        try:
            current_temp = get_latest_zone_temp()
            print("Current zone temp:", current_temp)
            heating_sp, cooling_sp = compute_setpoints(current_temp)
            print("Computed setpoints:", heating_sp, cooling_sp)
            write_setpoint_to_bacnet(DEVICE_ID, 'presentValue_heating_setpoint', heating_sp)
            write_setpoint_to_bacnet(DEVICE_ID, 'presentValue_cooling_setpoint', cooling_sp)
            save_setpoint_to_db(ZONE_NAME, heating_sp, cooling_sp)
        except Exception as e:
            print("Controller error:", e)
        time.sleep(poll_interval)

if __name__ == "__main__":
    controller_loop()
