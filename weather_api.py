import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()  # Load .env file

GEOCODE_API = os.getenv("GEOCODE_API")
WEATHER_API = os.getenv("WEATHER_API")

# Rate limiting for Nominatim (1 request per second)
_last_geocode_request = 0

weather_text = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Partly Cloudy",
    45: "Fog",
    48: "Fog",
    51: "Drizzle",
    53: "Drizzle",
    55: "Drizzle",
    56: "Freezing Drizzle",
    57: "Freezing Drizzle",
    61: "Rain",
    63: "Rain",
    65: "Rain",
    66: "Freezing Rain",
    67: "Freezing Rain",
    71: "Snow",
    73: "Snow",
    75: "Snow",
    77: "Snow Grains",
    80: "Rain Showers",
    81: "Rain Showers",
    82: "Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Thunderstorm with Hail"
}

weather_icons = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "⛅",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    53: "🌦️",
    55: "🌦️",
    56: "🌧️",
    57: "🌧️",
    61: "🌧️",
    63: "🌧️",
    65: "🌧️",
    66: "🌧️",
    67: "🌧️",
    71: "❄️",
    73: "❄️",
    75: "❄️",
    77: "❄️",
    80: "🌦️",
    81: "🌦️",
    82: "🌦️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️"
}

# Fallback coordinates for major Pakistani cities
CITY_COORDINATES = {
    "Lahore": (31.5204, 74.3587),
    "Karachi": (24.8607, 67.0011),
    "Islamabad": (33.6844, 73.0479),
    "Quetta": (30.1798, 66.9750),
    "Peshawar": (34.0151, 71.5249),
    "Multan": (30.1575, 71.5249),
    "Faisalabad": (31.4504, 73.1350),
    "Sialkot": (32.4945, 74.5229)
}

def get_coordinates(city):
    global _last_geocode_request
    
    # First, check if we have a hardcoded fallback for this city
    if city in CITY_COORDINATES:
        lat, lon = CITY_COORDINATES[city]
        return lat, lon
    
    # Use Nominatim API if GEOCODE_API is not set
    if GEOCODE_API:
        # Custom API endpoint format
        url = f"{GEOCODE_API}?city={city}&country=Pakistan&format=json"
        headers = {
            "User-Agent": "ClimateHubApp/1.0 (contact@example.com)"
        }
    else:
        # Default to Nominatim OpenStreetMap API
        url = f"https://nominatim.openstreetmap.org/search?q={city},Pakistan&format=json&limit=1"
        headers = {
            "User-Agent": "ClimateHubApp/1.0 (contact@example.com)",
            "Accept-Language": "en"
        }
        # Rate limiting: Nominatim requires max 1 request per second
        current_time = time.time()
        time_since_last = current_time - _last_geocode_request
        if time_since_last < 1.0:
            time.sleep(1.0 - time_since_last)
        _last_geocode_request = time.time()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            if response.status_code == 403:
                print("Error: API access forbidden. Using fallback coordinates if available.")
                # Try fallback even if API fails
                if city in CITY_COORDINATES:
                    return CITY_COORDINATES[city]
            return None, None

        # Only parse JSON if content exists
        if response.text.strip() == "":
            print("Error: Empty response from geocoding API")
            return None, None

        data = response.json()
        if data and len(data) > 0:
            # Handle both custom API format and Nominatim format
            if isinstance(data, list) and len(data) > 0:
                if 'lat' in data[0] and 'lon' in data[0]:
                    return float(data[0]['lat']), float(data[0]['lon'])
            elif isinstance(data, dict) and 'lat' in data and 'lon' in data:
                return float(data['lat']), float(data['lon'])
        
        print("Error: No valid coordinates returned for city")
        return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates (network): {e}")
        # Try fallback on network error
        if city in CITY_COORDINATES:
            return CITY_COORDINATES[city]
        return None, None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error parsing coordinates: {e}")
        return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None


def get_current_weather(lat, lon):
    """Get current weather from Open-Meteo"""
    url = f"{WEATHER_API}?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url)
        data = response.json()
        if 'current_weather' in data:
            return data['current_weather']
    except Exception as e:
        print("Error fetching weather:", e)
    return None

def get_5day_forecast(lat, lon):
    """Get 5-day weather forecast"""
    url = f"{WEATHER_API}?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Karachi"
    try:
        response = requests.get(url)
        data = response.json()
        if 'daily' in data:
            return data['daily']
    except Exception as e:
        print("Error fetching 5-day forecast:", e)
    return None

def get_weather_icon(code):
    return weather_icons.get(code, "🌡️")

def get_weather_text(code):
    return weather_text.get(code, "Unknown")

