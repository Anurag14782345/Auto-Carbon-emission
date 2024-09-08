from flask import Flask, jsonify
from flask_cors import CORS
import serial

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

# Attempt to open the serial connection
try:
    ser = serial.Serial('COM3', 115200, timeout=2)  # Added timeout for safety
    print("Serial port connected")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    ser = None  # Handle this gracefully in your Flask routes

# Define normal thresholds for CO and flammable gases
CO_NORMAL_THRESHOLD = 0.5  # Example threshold for CO in % or g/mile
FLAMMABLE_GAS_NORMAL_THRESHOLD = 200  # Example threshold for flammable gas in ppm

@app.route('/gas-data', methods=['GET'])
def get_gas_data():
    if ser is None:
        print("Serial connection failed.")
        return jsonify({'error': 'Serial connection failed'}), 500
    
    try:
        if ser.in_waiting > 0:
            # Read data and split it
            data = ser.readline().decode('utf-8').strip().split(',')
            print(f"Raw data from sensor: {data}")  # For debugging

            if len(data) != 2:
                print("Invalid data format received from sensor")
                return jsonify({'error': 'Invalid data format'}), 400

            co_value = float(data[0])
            flammable_gas_value = int(data[1])

            # Determine gas statuses
            co_status = "Normal" if co_value < CO_NORMAL_THRESHOLD else "High"
            gas_status = "Normal" if flammable_gas_value < FLAMMABLE_GAS_NORMAL_THRESHOLD else "High"

            return jsonify({
                'co_value': co_value,
                'flammable_gas_value': flammable_gas_value,
                'co_status': co_status,
                'gas_status': gas_status
            })
        else:
            print("No data available from sensor")
            return jsonify({'error': 'No data available from sensor'}), 500

    except ValueError as e:
        print(f"ValueError: {e}")
        return jsonify({'error': 'Error parsing data'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
