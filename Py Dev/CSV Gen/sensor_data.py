import serial
import time
import csv
from datetime import datetime

# Open serial connection
ser = serial.Serial('COM3', 115200)

# Initialize variables to store data
sensor_data = []
start_time = time.time()

def write_to_csv(data):
    print("Writing data to CSV...")  # Debugging
    # Write data to CSV
    with open('sensor_data.csv', mode='a', newline='') as file:  # Changed to 'a' to append data
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty and write the header if true
            writer.writerow(['Timestamp', 'CO Value', 'Flammable Gas Value'])  # Header
        writer.writerows(data)
    print("Data written to CSV")

try:
    while True:
        if ser.in_waiting > 0:
            print("Reading serial data...")  # Debugging
            # Read data from serial and timestamp it
            raw_data = ser.readline().decode('utf-8').strip().split(',')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if len(raw_data) == 2:
                try:
                    co_value = float(raw_data[0])
                    flammable_gas_value = int(raw_data[1])
                    
                    # Append the data along with the timestamp
                    sensor_data.append([timestamp, co_value, flammable_gas_value])
                    print(f"Data appended: {timestamp}, {co_value}, {flammable_gas_value}")  # Debugging
                except ValueError as e:
                    print(f"Data conversion error: {e} - Data received: {raw_data}")
            
            # Check if a minute has passed
            if time.time() - start_time >= 60:
                print("One minute passed, writing data to CSV")  # Debugging
                # Write data to CSV and clear memory
                write_to_csv(sensor_data)
                sensor_data = []  # Clear old data
                start_time = time.time()  # Reset timer
except serial.SerialException as e:
    print(f"Serial error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    # Ensure the serial connection is properly closed
    if ser.is_open:
        ser.close()
        print("Serial connection closed.")
