from agents.tools.base import BaseTool
from agents.utils.api_client import APIClient
from typing import Dict, Any


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
        return "get_restaurant_detail"
    
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
            return await self.api_client.get(f"/restaurants/{kwargs['restaurant_id']}/tables")
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
                "cuisine_type": {"type": "string", "enum": ["NORTH_INDIAN", "SOUTH_INDIAN", "CHINESE", "ITALIAN", "JAPANESE"], "description": "Type of cuisine"},
                "price_range": {"type": "string", "enum": ["$", "$$", "$$$", "$$$$"], "description": "Price category"},
                "ambiance": {"type": "string", "enum": ["CASUAL", "FORMAL", "FAMILY", "ROMANTIC"], "description": "Restaurant atmosphere"},
                "min_seating": {"type": "integer", "description": "Minimum seating capacity required"},
                "special_event_space": {"type": "boolean", "description": "Whether special events can be hosted"},
                "dietary_options": {"type": "string", "description": "Specific dietary requirements"},
                "area": {"type": "string", "description": "Location/area of the restaurant"},
                "skip": {"type": "integer", "default": 0},
                "limit": {"type": "integer", "default": 100}
            }
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return self.api_client.get("/restaurants/search", params=kwargs)
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

class CreateCustomerTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_customer"
    
    @property
    def description(self) -> str:
        return "Register a new customer"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Customer's full name"},
                "phone": {"type": "string", "description": "Contact number"},
                "email": {"type": "string", "description": "Email address"}
            },
            "required": ["name", "phone"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.post("/customers/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}
        
class GetCustomerByPhone(BaseTool):
    @property
    def name(self) -> str:
        return "get_customer_by_phone"
    
    @property
    def description(self) -> str:
        return "Get customer details by phone number"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "Customer's phone number"}
            },
            "required": ["phone"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.get("/customers/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}
        
class GetCustomerByEmail(BaseTool):
    @property
    def name(self) -> str:
        return "get_customer_by_email"
    
    @property
    def description(self) -> str:
        return "Get customer details by email address"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Customer's email address"}
            },
            "required": ["email"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.get("/customers/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}

class CreateReservationTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_reservation"
    
    @property
    def description(self) -> str:
        return "Create a new reservation"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "customer_id": {"type": "integer", "description": "ID of the customer making the reservation"},
                "restaurant_id": {"type": "integer", "description": "ID of the restaurant"},
                "table_id": {"type": "integer", "description": "ID of the table to reserve"},
                "reservation_date": {"type": "string", "format": "date", "description": "Date of the reservation"},
                "reservation_time": {"type": "string", "format": "time", "description": "Time of the reservation"},
                "number_of_guests": {"type": "integer", "description": "Number of people"},
                "special_requests": {"type": "string", "description": "Any special requirements"},
                "status": {"type": "string", "enum": ["CONFIRMED", "CANCELLED", "PENDING"], "description": "Status of the reservation"}
            },
            "required": ["customer_id", "restaurant_id", "table_id", "reservation_date", "reservation_time", "number_of_guests"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.post("/reservations/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}

class UpdateReservationStatusTool(BaseTool):
    @property
    def name(self) -> str:
        return "update_reservation_status"
    
    @property
    def description(self) -> str:
        return "Update the status of a reservation"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "reservation_id": {"type": "integer", "description": "ID of the reservation"},
                "status": {"type": "string", "enum": ["CONFIRMED", "CANCELLED", "PENDING"], "description": "New status"}
            },
            "required": ["reservation_id", "status"]
        }

    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.put(f"/reservations/{kwargs['reservation_id']}", params=kwargs)
        except Exception as e:
            return {"error": str(e)}
        

class GetReservationStatus(BaseTool):
    @property
    def name(self) -> str:
        return "get_reservation_status"
    
    @property
    def description(self) -> str:
        return "Get the status of a reservation"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "reservation_id": {"type": "integer", "description": "ID of the reservation"}
            },
            "required": ["reservation_id"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.get(f"/reservations/{kwargs['reservation_id']}/status")
        except Exception as e:
            return {"error": str(e)}