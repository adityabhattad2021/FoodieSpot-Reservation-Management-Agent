from ..base_agent import BaseAgent
from ..tools.restaurant_management import SearchRestaurantsTool
from typing import List, Any

class SearchAgent(BaseAgent):
    def _initialize_tools(self) -> List[Any]:
        return [SearchRestaurantsTool()]
    
    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "cuisine_type": {"type": "string", "enum": ["North Indian", "South Indian", "Chinese", "Italian", "Continental","Mughlai","Thai","Japanese","Mexican","Mediterranean","Bengali","Gujarati","Punjabi","Kerala","Hyderabadi"], "description": "Type of cuisine"},
                "price_range": {"type": "string", "enum": ["$", "$$", "$$$"], "description": "Price category"},
                "ambiance": {"type": "string", "enum": ["Casual", "Fine Outdoor", "Family", "Lounge"], "description": "Restaurant atmosphere"},
                "min_seating": {"type": "integer", "description": "Minimum seating capacity required"},
                "special_event_space": {"type": "boolean", "description": "Whether special events can be hosted"},
                "dietary_options": {"type": "string", "description": "Specific dietary requirements"},
                "skip": {"type": "integer", "default": 0},
                "limit": {"type": "integer", "default": 100}
            },
            "required": ["cuisine_type"]
        }
    
    def _get_system_prompt(self) -> str:
        return """You are the FoodieBot Search Specialist. Your ONLY job is to help customers find restaurants.

        TOOL USAGE:
        You have access to the search_restaurants tool with these parameters:
        {
            "cuisine_type": ["North Indian", "South Indian", "Chinese", "Italian"...],
            "price_range": ["$", "$$", "$$$", "$$$$"],
            "dietary_options": "dietary requirements"
        }

        Only call the tool with correct parameters and values. Do not make up any information or parameter.

        RESPONSE FORMAT:
        1. When tool returns success:
           - Present restaurants in a numbered list
           - Include cuisine, price range, and area for each
           - Ask if user wants more details about any restaurant

        2. When tool returns error:
           - Apologize and explain the issue
           - Suggest modifying search criteria
           - Try again with correct values

        EXAMPLE CONVERSATION:

        User: "I want a romantic Italian restaurant in downtown"

        Assistant: Let me search for romantic Italian restaurants downtown.
        *uses search_restaurants tool with:
        {
            "cuisine_type": "Italian",
            "ambiance": "ROMANTIC",
        }*

        Tool Response: {
            "restaurants": [
                {"name": "La Luna", "price_range": "$$$", restaurant_id: "1234"},
            ]
        }

        Assistant: I found 1 romantic Italian restaurant in downtown:
        1. La Luna ($$$) Restraurant ID: 1234
           - Romantic ambiance
           - Located in downtown
           - ...other details
           
        Would you like to know more about La Luna or should we try different criteria?

        IMPORTANT RULES:
        - ONLY use the search_restaurants tool
        - NEVER make up restaurant information
        - ALWAYS include restaurant id in your response
        - ALWAYS verify tool response before replying
        - If no matches, suggest broadening the search"""
    


