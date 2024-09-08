import serial

try:
    ser = serial.Serial('COM3', 115200)
    while True:
        if ser.in_waiting > 0:
            print(ser.readline().decode('utf-8').strip())
except serial.SerialException as e: 
    print(f"Error: {e}")
