import pandas as pd
import random
vehicle_types = ["Car", "Bike", "SUV", "Truck"]
weather_conditions = ["Sunny", "Rainy", "Foggy", "Snowy"]
traffic_conditions = ["Low", "Medium", "High"]
location_types = ["Residential", "Office", "Shopping Mall"]

data = []
for i in range(1000):
    vehicle_number = f"ABC{random.randint(1000, 9999)}"
    vehicle_type = random.choice(vehicle_types)
    weather = random.choice(weather_conditions)
    traffic = random.choice(traffic_conditions)
    location = random.choice(location_types)

    if location == "Office":
        parking_time = random.randint(4, 8)
    elif location == "Shopping Mall":
        parking_time = random.randint(1, 3)
    else:
        parking_time = random.randint(6, 12)

    if traffic == "High":
        parking_time += 1
    if weather in ["Rainy", "Foggy"]:
        parking_time += 1

    data.append([vehicle_number, vehicle_type, weather, traffic, location, parking_time])

df = pd.DataFrame(data, columns=["Vehicle Number", "Vehicle Type", "Weather", "Traffic", "Location", "Parking Time"])
df.to_csv("data/parking_data.csv", index=False)
