from typing import Optional, List, Dict, Any
from datetime import datetime
from groq import Groq
from pydantic import BaseModel, Field
import instructor
from agents.tools.restaurants.tools import (
    SearchRestaurantsTool,
    GetAvailableRestaurantsTool,
)
from agents.tools.reservations.tools import (
    CreateReservationTool,
    CancelReservationTool,
    CheckReservationTool
)
from agents.utils.api_client import APIClient
from agents.config import settings
import logging
import json
import httpx

class RestaurantRequest(BaseModel):
    cuisine_preferences: Optional[List[str]] = Field(None, description="Preferred types of cuisine")
    price_range: Optional[str] = Field(None, description="Preferred price range ($, $$, $$$, $$$$)")
    party_size: Optional[int] = Field(None, description="Number of people in the party")
    area: Optional[str] = Field(None, description="Preferred location/area")
    special_occasion: bool = Field(False, description="Whether it's a special occasion")
    reservation_date: Optional[str] = Field(None, description="Desired reservation date (YYYY-MM-DD)")
    reservation_time: Optional[str] = Field(None, description="Desired reservation time (HH:MM)")

class ConversationResponse(BaseModel):
    message: str = Field(..., description="The response message to show to the user")
    conversation_ended: bool = Field(False, description="Whether the conversation should end")
    requires_tool: bool = Field(False, description="Whether a tool was used in generating this response")
    thought: Optional[str] = Field(None, description="The agent's reasoning")
    action: Optional[str] = Field(None, description="The tool action to execute")
    action_input: Optional[Dict[str, Any]] = Field(None, description="The input parameters for the tool")
    is_final_answer: bool = Field(False, description="Whether this is the final answer")

class RestaurantAgent:
    def __init__(self):
        # Initialize API clients
        self.api_client = APIClient(base_url=settings.API_BASE_URL)
        self.llm_client = instructor.from_groq(Groq(api_key=settings.GROQ_API_KEY), mode=instructor.Mode.JSON)
        
        # Initialize tools
        self.tools = [
            SearchRestaurantsTool(self.api_client),
            GetAvailableRestaurantsTool(self.api_client),
            CreateReservationTool(self.api_client),
            CancelReservationTool(self.api_client),
            CheckReservationTool(self.api_client)
        ]

        self.conversation_history = []

    def _get_system_prompt(self) -> str:
        return """You are a helpful restaurant booking assistant named Pankaj Shastri that helps users find and book restaurants. 
        You run in a loop of Thought, Action, PAUSE, Observation.

        At each step:
        1. Use Thought to describe your reasoning about what to do next
        2. Use Action to specify which tool to run with what parameters - then return PAUSE
        3. You will receive an Observation with the result
        4. When you have a final answer, output it as Answer: followed by your response

        Your available tools are:

        search_restaurants:
        Parameters: {"cuisine_type": "string?", "price_range": "string?", "area": "string?"}
        Returns: List of matching restaurants
        Example: Action: search_restaurants: {"cuisine_type": "Italian", "price_range": "$$"}

        get_available_restaurants:
        Parameters: {"date": "YYYY-MM-DD", "time": "HH:MM", "party_size": number}
        Returns: List of available restaurants with times
        Example: Action: get_available_restaurants: {"date": "2024-03-20", "time": "19:00", "party_size": 4}

        create_reservation:
        Parameters: {"restaurant_id": number, "date": "YYYY-MM-DD", "time": "HH:MM", "party_size": number, "customer_id": number, "table_id": number}
        Creates a reservation
        Example: Action: create_reservation: {"restaurant_id": 123, "date": "2024-03-20", "time": "19:00", "party_size": 4, "customer_id": 789, "table_id": 45}

        cancel_reservation:
        Parameters: {"reservation_id": number}
        Cancels a reservation
        Example: Action: cancel_reservation: {"reservation_id": 456}

        check_reservation:
        Parameters: {"reservation_id": number}
        Checks reservation status
        Example: Action: check_reservation: {"reservation_id": 456}

        Example conversation:

        User: I'd like to find an Italian restaurant for tomorrow night
        Thought: I should search for Italian restaurants first
        Action: search_restaurants: {"cuisine_type": "Italian"}
        PAUSE

        Observation: [{"id": 123, "name": "Bella Italia", "price_range": "$$", "rating": 4.5}]

        Thought: Now I need to check availability for tomorrow night
        Action: get_available_restaurants: {"date": "2024-03-20", "time": "19:00", "party_size": 2}
        PAUSE

        Observation: [{"restaurant_id": 123, "available_times": ["18:30", "19:00", "19:30"]}]

        Answer: I found Bella Italia, a $$-rated Italian restaurant with availability tomorrow at 18:30, 19:00, and 19:30. Would you like me to make a reservation?

        Remember to:
        1. Think through each step logically
        2. Use the appropriate tool for each action
        3. Provide clear, helpful responses
        4. Ask for any missing information needed
        5. Handle errors gracefully"""

    async def _execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return {"error": f"Tool {tool_name} not found"}
        return await tool.execute(**kwargs)

    async def process_request(self, user_input: str, request_data: RestaurantRequest) -> ConversationResponse:
        try:
            if user_input:
                self.conversation_history.append({"role": "user", "content": str(user_input)})
            
            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                *self.conversation_history
            ]
            
            response = None
            max_iterations = 20
            iteration = 0
            
            while iteration < max_iterations:
                # Get LLM response
                response = self.llm_client.chat.completions.create(
                    model=settings.DEFAULT_MODEL,
                    messages=messages,
                    response_model=ConversationResponse,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                # If we need to use a tool
                if response.action and response.action_input:
                    observation = await self._execute_tool(response.action, **response.action_input)
                    messages.append({
                        "role": "system",
                        "content": f"Observation: {json.dumps(observation)}"
                    })
                # If we have a final answer, break
                elif response.is_final_answer:
                    break
                
                iteration += 1
            
            # Add final response to history
            if response and response.message:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": str(response.message)
                })
            
            return response

        except Exception as e:
            logger.error("Error in process_request", exc_info=True)
            raise

    async def close(self):
        self.conversation_history.clear()
        await self.api_client.close()