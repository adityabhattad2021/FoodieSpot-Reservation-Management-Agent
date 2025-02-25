from typing import Dict, Tuple, Any

from ..tools.base_tool import BaseTool


class CreateRestaurantTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_restaurant"
    
    @property
    def description(self) -> str:
        return "Create a new restaurant with specified details"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Restaurant name"},
                "address": {"type": "string", "description": "Physical location"},
                "phone": {"type": "string", "description": "Contact number"},
                "email": {"type": "string", "description": "Contact email"},
                "opening_time": {"type": "string", "format": "time", "description": "Daily opening time"},
                "closing_time": {"type": "string", "format": "time", "description": "Daily closing time"},
                "seating_capacity": {"type": "integer", "description": "Total capacity"},
                "special_event_space": {"type": "boolean", "description": "Whether special events can be hosted"}
            },
            "required": ["name", "address", "phone", "opening_time", "closing_time", "seating_capacity"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.post("/restaurants/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}


class ListRestaurantsTool(BaseTool):
    @property
    def name(self) -> str:
        return "list_restaurants"
    
    @property
    def description(self) -> str:
        return "Retrieve a list of all restaurants with pagination support"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "skip": {"type": "integer", "description": "Number of records to skip", "default": 0},
                "limit": {"type": "integer", "description": "Maximum number of records to return", "default": 100}
            }
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.get("/restaurants/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}

class GetRestaurantTableTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_restaurant_table"
    
    @property
    def description(self) -> str:
        return "Get all available tables for the restraurant"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "integer", "description": "ID of the restaurant"}
            },
            "required": ["restaurant_id"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.get(f"/restaurants/{kwargs['restaurant_id']}/tables/")
        except Exception as e:
            return {"error": str(e)}

class SearchRestaurantsTool(BaseTool):
    @property
    def name(self) -> str:
        return "search_restaurants"
    
    @property
    def description(self) -> str:
        return "Search restaurants with multiple filters"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "cuisine_type": {"type": "string", "enum": ["North Indian", "South Indian", "Chinese", "Italian", "Continental","Mughlai","Thai","Japanese","Mexican","Mediterranean","Bengali","Gujarati","Punjabi","Kerala","Hyderabadi"], "description": "Type of cuisine"},
                "price_range": {"type": "string", "enum": ["$", "$$", "$$$", "$$$$"], "description": "Price category"},
                "ambiance": {"type": "string", "enum": ["Casual", "Fine Outdoor", "Family", "Lounge"], "description": "Restaurant atmosphere"},
                "min_seating": {"type": "integer", "description": "Minimum seating capacity required"},
                "special_event_space": {"type": "boolean", "description": "Whether special events can be hosted"},
                "dietary_options": {"type": "string", "description": "Specific dietary requirements"},
                "skip": {"type": "integer", "default": 0},
                "limit": {"type": "integer", "default": 100}
            }
        }
    
  
class SearchRestaurantsTool(BaseTool):
    @property
    def name(self) -> str:
        return "search_restaurants"

    @property
    def description(self) -> str:
        return "Search restaurants with multiple filters"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "cuisine_type": {
                    "type": "string",
                    "enum": [
                        "North Indian", "South Indian", "Chinese", "Italian", "Continental", "Mughlai", "Thai",
                        "Japanese", "Mexican", "Mediterranean", "Bengali", "Gujarati", "Punjabi", "Kerala", "Hyderabadi"
                    ],
                    "description": "Type of cuisine"
                },
                "price_range": {
                    "type": "string",
                    "enum": ["$", "$$", "$$$", "$$$$"],
                    "description": "Price category"
                },
                "ambiance": {
                    "type": "string",
                    "enum": ["Casual", "Fine Outdoor", "Family", "Lounge"],
                    "description": "Restaurant atmosphere"
                },
                "min_seating": {
                    "type": "integer",
                    "description": "Minimum seating capacity required"
                },
                "special_event_space": {
                    "type": "boolean",
                    "description": "Whether special events can be hosted"
                },
                "dietary_options": {
                    "type": "string",
                    "description": "Specific dietary requirements"
                },
                "skip": {
                    "type": "integer",
                    "default": 0
                },
                "limit": {
                    "type": "integer",
                    "default": 100
                }
            }
        }

    def validate_params(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """ Validates input parameters before making an API call. """
        valid_keys = {
            "cuisine_type", "price_range", "ambiance", "min_seating",
            "special_event_space", "dietary_options", "skip", "limit"
        }
        valid_cuisines = [
            "North Indian", "South Indian", "Chinese", "Italian", "Continental", "Mughlai", "Thai",
            "Japanese", "Mexican", "Mediterranean", "Bengali", "Gujarati", "Punjabi", "Kerala", "Hyderabadi"
        ]
        valid_price_ranges = ["$", "$$", "$$$", "$$$$"]
        valid_ambiances = ["Casual", "Fine Outdoor", "Family", "Lounge"]

        invalid_keys = [key for key in params if key not in valid_keys]
        if invalid_keys:
            return False, f"Invalid keys found: {invalid_keys}. Allowed keys are {valid_keys}."

        if "cuisine_type" in params and params["cuisine_type"] not in valid_cuisines:
            return False, f"Invalid cuisine_type: '{params['cuisine_type']}'. Must be one of {valid_cuisines}."

        if "price_range" in params and params["price_range"] not in valid_price_ranges:
            return False, f"Invalid price_range: '{params['price_range']}'. Must be one of {valid_price_ranges}."

        if "ambiance" in params and params["ambiance"] not in valid_ambiances:
            return False, f"Invalid ambiance: '{params['ambiance']}'. Must be one of {valid_ambiances}."

        if "min_seating" in params:
            if not isinstance(params["min_seating"], int) or params["min_seating"] <= 0:
                return False, f"Invalid min_seating: '{params['min_seating']}'. Must be a positive integer."

        if "special_event_space" in params and not isinstance(params["special_event_space"], bool):
            return False, f"Invalid special_event_space: '{params['special_event_space']}'. Must be true or false."

        if "skip" in params:
            if not isinstance(params["skip"], int) or params["skip"] < 0:
                return False, f"Invalid skip value: '{params['skip']}'. Must be a non-negative integer."

        if "limit" in params:
            if not isinstance(params["limit"], int) or params["limit"] <= 0:
                return False, f"Invalid limit value: '{params['limit']}'. Must be a positive integer."

        return True, "Parameters are valid."

    def execute(self, **kwargs) -> Dict[str, Any]:
        """ Executes the restaurant search after validating parameters. """
        is_valid, message = self.validate_params(kwargs)
        if not is_valid:
            return {"error": message}

        try:
            return self.api_client.get("/restaurants/search/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}

class GetAvailableRestaurantsTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_available_restaurants"
    
    @property
    def description(self) -> str:
        return "Get restaurants that have available tables for the specified date, time and party size"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "reservation_date": {"type": "string", "format": "date", "description": "Date of reservation"},
                "reservation_time": {"type": "string", "format": "time", "description": "Time of reservation"},
                "party_size": {"type": "integer", "description": "Number of people"},
                "skip": {"type": "integer", "default": 0},
                "limit": {"type": "integer", "default": 100}
            },
            "required": ["reservation_date", "reservation_time", "party_size"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return self.api_client.get("/restaurants/available/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}

class CreateTableTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_table"
    
    @property
    def description(self) -> str:
        return "Create a new table in a restaurant"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "integer", "description": "ID of the restaurant"},
                "table_number": {"type": "integer", "description": "Unique number within the restaurant"},
                "seating_capacity": {"type": "integer", "description": "Number of seats at the table"},
                "table_type": {"type": "string", "enum": ["REGULAR", "BOOTH", "PRIVATE"], "description": "Type of table"},
                "status": {"type": "string", "enum": ["AVAILABLE", "RESERVED", "MAINTENANCE"], "description": "Current status"}
            },
            "required": ["restaurant_id", "table_number", "seating_capacity", "table_type"]
        }