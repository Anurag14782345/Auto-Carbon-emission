import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
