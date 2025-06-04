from typing import Any
from smolagents.tools import Tool
import datetime
import pytz

class GetCurrentTimeInTimezoneTool(Tool):
    name = "get_current_time_in_timezone"
    description = "A tool that fetches the current local time in a specified timezone."
    inputs = {'timezone': {'type': 'string', 'description': 'A string representing a valid timezone (e.g., \'America/New_York\').', 'nullable': True}}
    output_type = "string"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_initialized = True

    def forward(self, timezone: str = None) -> str:
        try:
            # Handle nullable timezone
            if timezone is None:
                timezone = "UTC"
                
            # Create timezone object
            tz = pytz.timezone(timezone)
            # Get current time in that timezone
            local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            return f"The current local time in {timezone} is: {local_time}"
        except Exception as e:
            return f"Error fetching time for timezone '{timezone}': {str(e)}"