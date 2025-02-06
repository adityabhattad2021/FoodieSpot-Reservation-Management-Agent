from typing import List, Dict, Any, Optional
from agents.core.config import settings
from agents.utils.api_client import APIClient
from groq import Groq
from agents.tools.tools import (
    GetCustomerByEmail,
    GetCustomerByPhone,
    UpdateReservationStatusTool,
    GetAvailableRestaurantsTool,
    GetRestaurantTableTool,
    SearchRestaurantsTool,
    CreateReservationTool,
    CreateCustomerTool,
    GetReservationStatus,
)
from pydantic import BaseModel, Field
import json

# Constants
MAX_CONVERSATION_HISTORY = 10
MAX_ITERATIONS = 5

class Message(BaseModel):
    role: str
    content: str


class RestaurantAgent:
    def __init__(self):
        self.llm_client = Groq(api_key=settings.GROQ_API_KEY)
        self.api_client = APIClient(base_url=settings.API_BASE_URL)
        self.conversation_history: List[Message] = []
        self.tools = self._initialize_tools()

    def _initialize_tools(self) -> List[Any]:
        return [
            SearchRestaurantsTool(self.api_client),
            GetRestaurantTableTool(self.api_client),
            GetCustomerByEmail(self.api_client),
            GetCustomerByPhone(self.api_client),
            CreateCustomerTool(self.api_client),
            CreateReservationTool(self.api_client),
            UpdateReservationStatusTool(self.api_client),
            GetReservationStatus(self.api_client),
        ]

    def _get_system_prompt(self) -> str:
        return f"""You are FoodieBot, an AI assistant for FoodieSpot restaurant booking service. Your job is to help customers find and book restaurants.
            Response Guidelines:
            Be Polite: Greet the customer warmly.
            Ask Questions: Find out what kind of restaurant they want, where, when, and for how many people.
            Use Tools: You have tools to help you. Use them when needed. Follow the examples *exactly*.
            Confirm: Always confirm details with the customer.
            End with a Friendly Closing: Thank the customer.
            IMPORTANT:  You MUST respond with a JSON object when using a tool.  The JSON must be valid.


            Example Conversation Flow:

            Customer: "I'm looking for a good Italian restaurant."

            FoodieBot: "Here are few italian restraurants:
            1. Giordano's
            2. Maggiano's"

            Customer: "I want to book a table for 4 people at Girodana."

            FoodieBot: "Great! . Let me check availability for tomorrow at 7pm. One moment please."

            FoodieBot: "I found a table for 4 at Giordano's. Would you like me to book it for you?"

            Customer: "Yes, please."

            FoodieBot: "Can you please provide your email address/phone number and name for the reservation?"

            Customer: "Yes sure, my email is aditya@email.com and name is Aditya."

            FoodieBot: "Thank you, Aditya. I have successfully booked a table for 4 at Giordano's for tomorrow at 7pm. You will receive a confirmation email shortly. Is there anything else I can help you with?"

            Customer: "No, that's all. Thank you!"

            FoodieBot: "You're welcome! Have a great day, Aditya. Goodbye!"
            """

    def _update_conversation_history(self, role: str, content: str) -> None:
        self.conversation_history.append(Message(role=role, content=content))
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY:]

    async def run(self, user_input: str) -> Dict[str, Any]:
        try:
            if not user_input.strip():
                return {"error": "Empty input received"}

            self._update_conversation_history("user", user_input)
            return await self._process_query()

        except Exception as e:
            raise e
            

    async def _process_query(self) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            *[msg.model_dump() for msg in self.conversation_history]
        ]

        for _ in range(MAX_ITERATIONS):
            response = self.llm_client.chat.completions.create(
                model=settings.DEFAULT_MODEL, 
                messages=messages,
                max_tokens=4096,
                tools=[tool.to_dict() for tool in self.tools], 
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            print("Calling tool" if tool_calls else "Tool not needed", tool_calls)
            if tool_calls:
                messages.append({"role":"assistant","tool_calls":[
                    {
                        "id":tool_call.id,
                        "function":{
                            "name":tool_call.function.name,
                            "arguments":tool_call.function.arguments
                        },
                        "type":tool_call.type
                    }
                    for tool_call in tool_calls
                ]})

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_arguments = tool_call.function.arguments
                    tool_result = await self._execute_tool(
                        function_name, function_arguments
                    )
                    messages.append({
                        "tool_call_id":tool_call.id,
                        "role":"tool",
                        "name":function_name,
                        "content":str(tool_result)
                    })
            
            else:
                messages.append({"role": "assistant", "content": response_message.content})
                self._update_conversation_history("assistant", response_message.content)
                break

        return {
            "message": response_message.content,
        }

    async def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return {"error": f"Tool {tool_name} not found"}
        try:
            params = json.loads(params)
            return await tool.execute(**params)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def close(self) -> None:
        self.conversation_history.clear()

async def test_agent_in_terminal():
    """Terminal-based testing interface for the RestaurantAgent"""
    agent = RestaurantAgent()
    print("\nWelcome to FoodieSpot Restaurant Assistant!")
    print("Type 'exit' to quit the conversation.\n")

    try:
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("\nGoodbye!")
                break
                
            response = await agent.run(user_input)
            
            if "error" in response:
                print(f"\nAssistant (Error): {response['error']}")
            else:
                print(f"\nAssistant: {response['message']}")
                
    except KeyboardInterrupt:
        print("\n\nConversation terminated by user.")
    finally:
        agent.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_in_terminal())