#!/usr/bin/env bash
set -e

# 1) Start DB
docker compose up -d

# 2) Wait a few seconds for DB to be ready
echo "Waiting for Postgres to start..."
sleep 5

# 3) Run EnergyPlus (blocking) -> generates CSV to ingest
python3 energyplus/run_energyplus.py || { echo "EnergyPlus failed or not installed. Skipping simulation."; }

# 4) Ingest CSV into DB
python3 db/ingest_energyplus_csv.py || echo "CSV ingest failed; ensure energyplus output exists"

# 5) Start BACnet simulator (background)
python3 bacnet_sim/bacnet_simulator.py & 
SIM_PID=$!
sleep 2
echo "BACnet simulator started (pid $SIM_PID)"

# 6) Start controller (foreground)
python3 controller/hvac_controller.py
