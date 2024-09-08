import json

# Load the sensor data from the JSON file
file_path = '../json/sensor_data.json'  # Adjusted path

def load_sensor_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Classify emissions based on CO levels
def classify_emission(co_level):
    if co_level <= 10:
        return "Safest"
    elif 10 < co_level <= 30:
        return "Normal"
    elif 30 < co_level <= 50:
        return "Average"
    elif 50 < co_level <= 100:
        return "Above Average"
    elif 100 < co_level <= 200:
        return "Danger"
    else:
        return "Hazardous"

# Calculate the average CO value and classify emissions based on it
def calculate_and_classify_emission(data):
    if not data:
        return []

    # Calculate average CO value
    total_co = sum(entry["co_value"] for entry in data)
    average_co = total_co / len(data)

    # Classify the average CO value
    classification = classify_emission(average_co)

    return {
        "average_co_value": average_co,
        "classification": classification
    }

# Display the classification results
def display_results(results):
    print(f"Average CO Value: {results['average_co_value']} ppm")
    print(f"Classification: {results['classification']}")

# Load and classify data
sensor_data = load_sensor_data(file_path)
results = calculate_and_classify_emission(sensor_data)
display_results(results)
