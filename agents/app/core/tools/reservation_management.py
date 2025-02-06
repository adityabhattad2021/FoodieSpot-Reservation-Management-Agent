from ..tools.base_tool import BaseTool
from typing import Dict, Any

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