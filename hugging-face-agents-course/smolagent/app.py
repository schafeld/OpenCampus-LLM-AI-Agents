from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
import os
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/Projekte/MOOC/OpenCampus/codespace/.env"))

if not os.environ.get("HF_TOKEN"):
  # os.environ["HF_TOKEN"] = getpass.getpass("Enter API key for Hugging Face: ")
  raise EnvironmentError("HF_TOKEN not found in the .env file.")

if not os.environ.get("OPEN_WEATHER_API_KEY"):
  # os.environ["OPEN_WEATHER_API_KEY"] = getpass.getpass("Enter API key for OpenWeather: ")
  raise EnvironmentError("OPEN_WEATHER_API_KEY not found in the .env file.")

if not os.environ.get("OPENAI_API_KEY"):
  # os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
  raise EnvironmentError("OPENAI_API_KEY not found in the .env file.")

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

@tool
def get_weather_by_city(city: str, country_code: str = "") -> str:
    """A tool that fetches current weather information for a specific city.
    Args:
        city: The name of the city (e.g., 'London', 'New York')
        country_code: Optional 2-letter country code (e.g., 'US', 'GB')
    """
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

@tool
def get_weather_forecast(city: str, country_code: str = "", days: int = 3) -> str:
    """A tool that fetches weather forecast for a specific city.
    Args:
        city: The name of the city (e.g., 'London', 'New York')
        country_code: Optional 2-letter country code (e.g., 'US', 'GB')
        days: Number of days to forecast (1-5, default: 3)
    """
    try:
        api_key = os.environ.get("OPEN_WEATHER_API_KEY")
        if not api_key:
            return "Error: OpenWeather API key not found"
        
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

@tool
def search_local_events(city: str, query: str = "events") -> str:
    """A tool that searches for local events in a specific city using web search.
    Args:
        city: The name of the city to search events in
        query: Optional search query to refine results (default: 'events')
    """
    try:
        # Use DuckDuckGo search to find local events
        search_tool = DuckDuckGoSearchTool()
        search_query = f"{query} in {city} today this week upcoming"
        
        results = search_tool(search_query)
        
        if not results or "No results found" in str(results):
            return f"No events found for '{query}' in {city}. Try searching with different keywords."
        
        return f"Local events in {city}:\n\n{results}"
        
    except Exception as e:
        return f"Error searching for events: {str(e)}"

@tool
def get_current_date_time() -> str:
    """A tool that returns the current date and time in UTC and local system time.
    """
    try:
        utc_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"Current UTC time: {utc_time}\nLocal system time: {local_time}"
    except Exception as e:
        return f"Error getting current time: {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[
        final_answer, 
        get_current_time_in_timezone,
        get_weather_by_city,
        get_weather_forecast,
        search_local_events,
        get_current_date_time,
        # my_custom_tool
    ], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()