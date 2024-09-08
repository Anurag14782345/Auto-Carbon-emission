import serial
import time
import json
import re
from datetime import datetime, timedelta

# Open serial connection
ser = serial.Serial('COM3', 115200)

# Initialize variables to store data
sensor_data = []
start_time = time.time()

# Regex pattern to extract CO and Flammable Gases values from the raw data
pattern = re.compile(r'CO: ([\d\.]+) ppm \| Flammable Gases: ([\d\.]+) ppm')

def write_to_json(data):
    print("Writing data to JSON...")  # Debugging
    # Load existing data (if the file exists)
    try:
        with open('sensor_data.json', 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Append new data to existing data
    if data:  # Only write if there's data
        existing_data.extend(data)
    
        # Write the updated data back to the JSON file
        with open('sensor_data.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

        print(f"Data written to JSON: {data}")  # Debugging
    else:
        print("No data to write!")  # If no data is available

def filter_old_data(data):
    """Filter out entries older than 3 minutes."""
    current_time = datetime.now()
    three_minutes_ago = current_time - timedelta(minutes=3)
    
    # Keep only data within the last 3 minutes
    return [entry for entry in data if datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S') > three_minutes_ago]

try:
    while True:
        if ser.in_waiting > 0:
            print("Reading serial data...")  # Debugging
            # Read data from serial and timestamp it
            raw_data = ser.readline().decode('utf-8').strip()
            print(f"Raw data received: {raw_data}")  # Debugging raw data
            
            # Extract CO and Flammable Gases values using regex
            match = pattern.search(raw_data)
            if match:
                co_value = float(match.group(1))
                flammable_gas_value = float(match.group(2))
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Append the data along with the timestamp in dictionary format
                sensor_data.append({
                    "timestamp": timestamp,
                    "co_value": co_value,
                    "flammable_gas_value": flammable_gas_value
                })
                print(f"Data appended: {timestamp}, {co_value}, {flammable_gas_value}")  # Debugging
            
            # Check if a minute has passed
            if time.time() - start_time >= 1:
                print("One minute passed, writing data to JSON")  # Debugging
                
                # Filter out entries older than 3 minutes
                sensor_data = filter_old_data(sensor_data)
                
                # Write data to JSON and clear memory
                write_to_json(sensor_data)
                start_time = time.time()  # Reset timer

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("Serial connection closed.")

finally:
    # Ensure the serial connection is properly closed
    if ser.is_open:
        ser.close()
        print("Serial connection closed.")
