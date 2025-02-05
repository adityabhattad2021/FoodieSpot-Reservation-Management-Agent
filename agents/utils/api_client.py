from typing import Optional, Dict, Any
from datetime import date, time
import httpx

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
    
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