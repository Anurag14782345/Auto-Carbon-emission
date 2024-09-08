from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Path to the JSON file
FILE_PATH = 'sensor_data.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        with open(FILE_PATH, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)