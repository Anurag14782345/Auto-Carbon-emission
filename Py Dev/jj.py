import serial
import time
import json
import re
from datetime import datetime, timedelta

ser = serial.Serial('COM3', 115200)

sensor_data = []
start_time = time.time()

pattern = re.compile(r'CO: ([\d\.]+) ppm \| Flammable Gases: ([\d\.]+) ppm')

def write_to_json(data):
    print("Writing data to JSON...")
    try:
        with open('sensor_data.json', 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    if data: 
        existing_data.extend(data)
        

        existing_data = filter_old_data(existing_data)
    

        with open('sensor_data.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

        print(f"Data written to JSON: {data}") 
        
    else:
        print("No data to write!")  
        
def filter_old_data(data):
    """Filter out entries older than 10 seconds."""
    current_time = datetime.now()
    ten_seconds_ago = current_time - timedelta(seconds=5)
    

    return [entry for entry in data if datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S') > ten_seconds_ago]

try:
    while True:
        if ser.in_waiting > 0:
            print("Reading serial data...")  
            
            raw_data = ser.readline().decode('utf-8').strip()
            print(f"Raw data received: {raw_data}")  
            
            match = pattern.search(raw_data)
            if match:
                co_value = float(match.group(1))
                flammable_gas_value = float(match.group(2))
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                sensor_data.append({
                    "timestamp": timestamp,
                    "co_value": co_value,
                    "flammable_gas_value": flammable_gas_value
                })
                print(f"Data appended: {timestamp}, {co_value}, {flammable_gas_value}")  # Debugging
            
            if time.time() - start_time >= 1:
                print("One minute passed, writing data to JSON")  
                
                write_to_json(sensor_data)
                start_time = time.time()  

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("Serial connection closed.")

finally:
    if ser.is_open:
        ser.close()
        print("Serial connection closed.")
