import requests
import random
import time
from datetime import datetime
import os
import sys

sys.stdout.reconfigure(line_buffering=True)

RUNNING_IN_DOCKER = os.path.exists('/.dockerenv') or os.getenv("RUNNING_IN_DOCKER") == "true"

if RUNNING_IN_DOCKER:
    API_URL = "http://flask_app:5000/store"
else:
    API_PORT = int(os.getenv("FLASK_PORT", 5001))
    API_URL = f"http://127.0.0.1:{API_PORT}/store"

SENSOR_ID = int(os.getenv("SENSOR_ID", 1))
SENSOR_TYPE = os.getenv("SENSOR_TYPE", "Temperature")

SENSOR_TYPES = {
    "Temperature": (10, 35, "°C"),
    "Pressure": (900, 1100, "hPa"),
    "Air Quality": (0, 150, "PM10"),
    "CO2": (300, 600, "ppm"),
}

def send_data(sensor_type):
    min_val, max_val, unit = SENSOR_TYPES[sensor_type]
    
    data = {
        "sensor_id": SENSOR_ID,
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "type": sensor_type,
        "value": round(random.uniform(min_val, max_val), 2)
    }

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=data, timeout=5)
            if response.status_code == 200:
                print(f"✔ Sent {sensor_type}: {data['value']} {unit}, Response: {response.status_code}")
                return
            else:
                print(f"⚠ Unexpected response {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"↻ [Sensor {SENSOR_ID}] Connection error to {API_URL}. Retrying {attempt + 1}/{max_retries}...")
        except requests.exceptions.Timeout:
            print(f"⌛ [Sensor {SENSOR_ID}] Timeout occurred. Retrying {attempt + 1}/{max_retries}...")
        except Exception as e:
            print(f"✗ [Sensor {SENSOR_ID}] Error sending data: {e}")
        time.sleep(3)
    print(f"✗ [Sensor {SENSOR_ID}] Max retries reached. Skipping this data point.")

print(f"▶ Starting sensor {SENSOR_ID} ({SENSOR_TYPE}) | API: {API_URL}")
while True:
    for sensor_type in SENSOR_TYPES.keys():
        send_data(sensor_type)
        time.sleep(5)