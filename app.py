from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import json
import random
from utils.weather_traffic import get_weather, get_traffic

app = Flask(__name__)

# Load ML model for parking time prediction
with open("models/parking_model.pkl", "rb") as f:
    model = pickle.load(f)

vehicle_types = ["Car", "Bike", "SUV", "Truck"]
location_types = ["Residential", "Office", "Shopping Mall"]

# Parking slot tracking (some slots are randomly occupied)
PARKING_SLOTS = {i: (1 if random.random() < 0.3 else 0) for i in range(1, 401)}  # 30% full slots

@app.route("/")
def home():
    return render_template("index.html", parking_slots=json.dumps(PARKING_SLOTS))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    vehicle_type = vehicle_types.index(data["vehicle_type"])
    location = location_types.index(data["location"])

    # Fetch weather & traffic data
    weather = get_weather()
    traffic = get_traffic()

    weather_conditions = ["Sunny", "Rainy", "Foggy", "Snowy"]
    traffic_conditions = ["Low", "Medium", "High"]

    weather_index = weather_conditions.index(weather) if weather in weather_conditions else 0
    traffic_index = traffic_conditions.index("Medium") if traffic == "Unknown" else (0 if traffic < 30 else 1 if traffic < 60 else 2)

    # Convert input into structured numpy array with correct feature names
    input_data = np.array([[vehicle_type, weather_index, traffic_index, location]], dtype=np.float32)
    
    # Ensure correct feature format for sklearn model
    input_data = np.array(input_data).reshape(1, -1)  # Reshape to 2D array

    predicted_time = model.predict(input_data)[0]

    # Assign the nearest available parking slot
    assigned_slot = None
    for slot, status in PARKING_SLOTS.items():
        if status == 0:  # Available slot
            PARKING_SLOTS[slot] = 1  # Mark as occupied
            assigned_slot = slot
            break

    if assigned_slot is None:
        return jsonify({'error': 'No available parking slots'}), 400

    return jsonify({
        "predicted_parking_time": round(predicted_time, 2),
        "weather": weather,
        "traffic": f"{traffic} km/h" if traffic != "Unknown" else "No data available",
        "assigned_slot": assigned_slot,
        "updated_slots": PARKING_SLOTS
    })

if __name__ == "__main__":
    app.run(debug=True)
