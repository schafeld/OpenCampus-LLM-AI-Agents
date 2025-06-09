from typing import Any
from smolagents.tools import Tool
import os
import requests

class GetWeatherByCityTool(Tool):
    name = "get_weather_by_city"
    description = "A tool that fetches current weather information for a specific city."
    inputs = {
        'city': {'type': 'string', 'description': 'The name of the city (e.g., \'London\', \'New York\')'},
        'country_code': {'type': 'string', 'description': 'Optional 2-letter country code (e.g., \'US\', \'GB\')', 'nullable': True}
    }
    output_type = "string"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_initialized = True

    def forward(self, city: str, country_code: str = None) -> str:
        try:
            api_key = os.environ.get("OPEN_WEATHER_API_KEY")
            if not api_key:
                return "Error: OpenWeather API key not found"
            
            # Build location string
            location = city
            if country_code:
                location += f",{country_code}"
            
            # Get current weather
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant information
            main = data['main']
            weather = data['weather'][0]
            wind = data.get('wind', {})
            
            weather_info = f"""Current weather in {data['name']}, {data['sys']['country']}:
- Temperature: {main['temp']}°C (feels like {main['feels_like']}°C)
- Condition: {weather['description'].title()}
- Humidity: {main['humidity']}%
- Pressure: {main['pressure']} hPa"""
            
            if 'speed' in wind:
                weather_info += f"\n- Wind Speed: {wind['speed']} m/s"
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
        except KeyError as e:
            return f"Error parsing weather data: Missing field {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"