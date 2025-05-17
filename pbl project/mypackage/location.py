import requests

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data['loc'].split(',')
        lat, lon = float(loc[0]), float(loc[1])
        return (lat, lon)
    except Exception as e:
        print("Error getting location:", e)
        return (0.0, 0.0)
