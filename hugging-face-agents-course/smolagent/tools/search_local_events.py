from typing import Any
from smolagents.tools import Tool
from smolagents import DuckDuckGoSearchTool

class SearchLocalEventsTool(Tool):
    name = "search_local_events"
    description = "A tool that searches for local events in a specific city using web search."
    inputs = {
        'city': {'type': 'string', 'description': 'The name of the city to search events in'},
        'query': {'type': 'string', 'description': 'Optional search query to refine results (default: \'events\')', 'nullable': True}
    }
    output_type = "string"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_initialized = True

    def forward(self, city: str, query: str = None) -> str:
        try:
            # Set default query if None
            if query is None:
                query = "events"
                
            # Use DuckDuckGo search to find local events
            search_tool = DuckDuckGoSearchTool()
            search_query = f"{query} in {city} today this week upcoming"
            
            results = search_tool(search_query)
            
            if not results or "No results found" in str(results):
                return f"No events found for '{query}' in {city}. Try searching with different keywords."
            
            return f"Local events in {city}:\n\n{results}"
            
        except Exception as e:
            return f"Error searching for events: {str(e)}"