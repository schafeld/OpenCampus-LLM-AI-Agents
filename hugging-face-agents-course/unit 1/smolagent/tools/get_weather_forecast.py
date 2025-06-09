from typing import Any
from smolagents.tools import Tool
import os
import requests
import datetime

class GetWeatherForecastTool(Tool):
    name = "get_weather_forecast"
    description = "A tool that fetches weather forecast for a specific city."
    inputs = {
        'city': {'type': 'string', 'description': 'The name of the city (e.g., \'London\', \'New York\')'},
        'country_code': {'type': 'string', 'description': 'Optional 2-letter country code (e.g., \'US\', \'GB\')', 'nullable': True},
        'days': {'type': 'integer', 'description': 'Number of days to forecast (1-5, default: 3)', 'nullable': True}
    }
    output_type = "string"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_initialized = True

    def forward(self, city: str, country_code: str = None, days: int = None) -> str:
        try:
            api_key = os.environ.get("OPEN_WEATHER_API_KEY")
            if not api_key:
                return "Error: OpenWeather API key not found"
            
            # Set default days if None
            if days is None:
                days = 3
            
            # Limit days to 5 (API limitation)
            days = min(max(1, days), 5)
            
            # Build location string
            location = city
            if country_code:
                location += f",{country_code}"
            
            # Get forecast
            url = f"https://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': location,
                'appid': api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecast_info = f"Weather forecast for {data['city']['name']}, {data['city']['country']}:\n\n"
            
            # Group forecasts by date
            daily_forecasts = {}
            for item in data['list'][:days*8]:  # 8 forecasts per day (3-hour intervals)
                date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(item)
            
            # Summarize each day
            for date, forecasts in list(daily_forecasts.items())[:days]:
                day_name = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %d')
                temps = [f['main']['temp'] for f in forecasts]
                conditions = [f['weather'][0]['description'] for f in forecasts]
                
                min_temp = min(temps)
                max_temp = max(temps)
                most_common_condition = max(set(conditions), key=conditions.count)
                
                forecast_info += f"📅 {day_name}:\n"
                forecast_info += f"   Temperature: {min_temp:.1f}°C - {max_temp:.1f}°C\n"
                forecast_info += f"   Condition: {most_common_condition.title()}\n\n"
            
            return forecast_info.strip()
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching forecast data: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"