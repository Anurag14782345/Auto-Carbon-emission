import serial

try:
    ser = serial.Serial('COM3', 115200)
    print("Serial port opened successfully.")
    ser.close()
except serial.SerialException as e:
    print(f"Error: {e}")
