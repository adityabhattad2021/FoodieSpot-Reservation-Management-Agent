from typing import Optional, Dict, Any
from ...config import settings
import httpx

class APIClient:
    def __init__(self):
        
        self.base_url = settings.API_BASE_URL.rstrip('/')
        self.api_key = settings.BACKEND_API_KEY
        self.client = httpx.AsyncClient(
            base_url=self.base_url, 
            timeout=30.0,
            headers=self._get_default_headers()
        )
    
    def _get_default_headers(self) -> Dict[str,str]:
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        await self.client.aclose()

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        return await self._make_request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Dict) -> Dict:
        return await self._make_request("POST", endpoint, json=json)

    async def put(self, endpoint: str, json: Dict) -> Dict:
        return await self._make_request("PUT", endpoint, json=json)

    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        json: Optional[Dict] = None
    ) -> Dict:
        try:
            response = await self.client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                params=params,
                json=json
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        
    async def get_user_details(self, user_id: str) -> Dict[str, Any]:
        if not user_id:
            return {"error": "User ID is required"}
        try:
            response = await self.get(f"/users/{user_id}")
            if "error" in response:
                return {"error": response["error"]}
            return response
        except Exception as e:
            return {"error": f"Failed to fetch user details: {str(e)}"}
        
    async def get_user_reservations(self, user_id: str) -> Dict[str, Any]:
        if not user_id:
            return {"error": "User ID is required"}
        try:
            response = await self.get(f"/users/{user_id}/reservations")
            if "error" in response:
                return {"error": response["error"]}
            return response
        except Exception as e:
            return {"error": f"Failed to fetch user reservations: {str(e)}"}
        
    async def make_reservation(self, reservation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a reservation using the backend API
        
        Args:
            reservation_data: Dictionary containing reservation details
                - restaurant_name: Name of the restaurant
                - date: Date in YYYY-MM-DD format
                - time: Time in HH:MM format
                - guests: Number of guests
                - user_id: ID of the user making the reservation
        
        Returns:
            Dictionary containing the reservation response or error
        """
        try:
            required_fields = ["restaurant_name", "date", "time", "guests"]
            for field in required_fields:
                if field not in reservation_data or not reservation_data[field]:
                    return {"error": f"Missing required field: {field}"}
            
            if "user_id" not in reservation_data or not reservation_data["user_id"]:
                return {"error": "User ID is required for making reservations"}
            
            response = await self.post("/book-restaurant/", json=reservation_data)
            
            if "error" in response:
                return {
                    "status": "error",
                    "message": response["error"],
                    "error_code": "API_ERROR"
                }
            
            return {
                "status": "success",
                "type": "success",
                "message": f"Your reservation at {response.get('restaurant_name')} for {response.get('guests')} people on {response.get('date')} at {response.get('time')} has been confirmed.",
                "reservation_code": response.get('reservation_code'),
                "restaurant": response.get('restaurant_name'),
                "date": response.get('date'),
                "time": response.get('time'),
                "party_size": response.get('guests')
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to make reservation: {str(e)}",
                "error_code": "SYSTEM_ERROR"
            }
        
    