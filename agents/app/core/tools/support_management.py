from .base_tool import BaseTool
from typing import Dict, Any
import datetime


class CreateSupportTicket(BaseTool):
    @property
    def name(self) -> str:
        return "create_support_ticket"
    
    @property
    def description(self) -> str:
        return "Create a new support ticket"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "customer_id": {"type": "integer", "description": "ID of the customer"},
                "ticket_description": {"type": "string", "description": "Description of the ticket"},
            },
            "required": ["customer_id","ticket_description"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        kwargs["ticket_date"] = datetime.datetime.now().date()
        kwargs["ticket_time"] = datetime.datetime.now().time()
        try:
            return await self.api_client.post("/support/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}
        
class CloseSupportTicket(BaseTool):
    @property
    def name(self) -> str:
        return "close_support_ticket"
    
    @property
    def description(self) -> str:
        return "Close an open support ticket"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer", "description": "ID of the support ticket"}
            },
            "required": ["ticket_id"]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            return await self.api_client.put(f"/support/{kwargs['ticket_id']}/close/")
        except Exception as e:
            return {"error": str(e)}