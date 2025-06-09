from typing import Any
from smolagents.tools import Tool
import datetime
from zoneinfo import ZoneInfo

class GetCurrentDateTimeTool(Tool):
    name = "get_current_date_time"
    description = "A tool that returns the current date and time in UTC and local system time."
    inputs = {}  # No inputs required for this tool
    output_type = "string"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_initialized = True

    def forward(self) -> str:
        try:
            # Use timezone-aware datetime
            utc_time = datetime.datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M:%S UTC")
            local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return f"Current UTC time: {utc_time}\nLocal system time: {local_time}"
        except Exception as e:
            return f"Error getting current time: {str(e)}"