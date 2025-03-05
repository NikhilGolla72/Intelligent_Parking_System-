import requests

OPENWEATHER_API_KEY ="YourApikey"
TOMTOM_API_KEY="YourApikey"

VELLORE_LAT, VELLORE_LON = 12.9165, 79.1325  # Vellore coordinates

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={VELLORE_LAT}&lon={VELLORE_LON}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if "weather" in response:
        return response["weather"][0]["main"]
    return "Unknown"

def get_traffic():
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={VELLORE_LAT},{VELLORE_LON}&key={TOMTOM_API_KEY}"
    response = requests.get(url).json()
    if "flowSegmentData" in response:
        return response["flowSegmentData"]["currentSpeed"]
    return "Unknown"

if __name__ == "__main__":
    print("Weather in Vellore:", get_weather())
    print("Traffic Speed in Vellore:", get_traffic(), "km/h")
