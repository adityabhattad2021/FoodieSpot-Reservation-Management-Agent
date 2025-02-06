from .base_tool import BaseTool
from typing import Dict, Any


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
            return await self.api_client.get("/customers/email/", params=kwargs)
        except Exception as e:
            return {"error": str(e)}