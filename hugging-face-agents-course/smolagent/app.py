from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
import os
from tools.final_answer import FinalAnswerTool
from tools.get_current_time_in_timezone import GetCurrentTimeInTimezoneTool
from tools.get_weather_by_city import GetWeatherByCityTool
from tools.get_weather_forecast import GetWeatherForecastTool
from tools.search_local_events import SearchLocalEventsTool
from tools.get_current_date_time import GetCurrentDateTimeTool

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

# Remove the @tool function definitions here and replace with tool instances
final_answer = FinalAnswerTool()
get_current_time_in_timezone = GetCurrentTimeInTimezoneTool()
get_weather_by_city = GetWeatherByCityTool()
get_weather_forecast = GetWeatherForecastTool()
search_local_events = SearchLocalEventsTool()
get_current_date_time = GetCurrentDateTimeTool()

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