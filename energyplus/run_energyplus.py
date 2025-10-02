import os
import subprocess
import shutil
import sys

EPLUS_PATH = os.getenv("ENERGYPLUS_BIN", "energyplus")  # ensure energyplus is on PATH
IDF_FILE = os.getenv("EPLUS_IDF", "energyplus/example.idf")
WEATHER_FILE = os.getenv("EPLUS_WEA", "energyplus/example.epw")
OUTPUT_DIR = os.getenv("EPLUS_OUT", "energyplus/ep_out")

def run():
    if not shutil.which(EPLUS_PATH):
        print("EnergyPlus executable not found. Please install EnergyPlus and ensure 'energyplus' is on PATH.")
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cmd = [EPLUS_PATH, "-w", WEATHER_FILE, "-d", OUTPUT_DIR, IDF_FILE]
    print("Running EnergyPlus:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("Simulation finished. Outputs in", OUTPUT_DIR)
    # Look for CSV or SQL outputs; EnergyPlus by default writes eplusout.csv or .eso; depending on idf requests.
    # For convenience, you can produce a csv using Output:Variable and the CSV output feature in the idf.

if __name__ == "__main__":
    run()
