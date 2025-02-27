from typing import Dict, Any

class CreateReservationTool():
    async def execute(self,reservation_details) -> Dict[str, Any]:
        try:
            return await self.api_client.post("/reservations/simple", params=reservation_details)
        except Exception as e:
            return {"error": str(e)}
