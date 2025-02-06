from typing import List, Dict, Any
from agents.core.config import settings
from agents.core.specialized.search_agent import SearchAgent
from groq import Groq
from pydantic import BaseModel

MAX_CONVERSATION_HISTORY = 10
MAX_ITERATIONS = 2

class Message(BaseModel):
    role: str
    content: str


class AgentTool:
    def __init__(self,name:str,agent:Any):
        self.name = name
        self.agent = agent

    def to_dict(self) -> Dict[str,Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": f"Use the {self.name} agent to handle {self.name}-related tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's request to be handled by the agent"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

class Router:
    def __init__(self):
        self.llm_client = Groq(api_key=settings.GROQ_API_KEY)
        self.tools = self._initialize_agent_tools()
        self.conversation_history: List[Message] = []
        
    def _initialize_agent_tools(self) -> List[AgentTool]:
        pass
        return [
            AgentTool("search_restraurant", SearchAgent()),
        #     AgentTool("table", TableAgent()),
        #     AgentTool("customer", CustomerAgent()),
        #     AgentTool("reservation", ReservationAgent())
        ]

    def _get_system_prompt(self) -> str:
        return """
        You are FoodieBot. Your job is to understand what the user wants and use the *best* tool to help with restaurants. If it's not about restaurants, or if you can answer the user directly, tell them what you can do.

        **TOOLS:**

        *   **search_restaurant:** Use this to find restaurants (cuisine, location, price).

        **RULES:**

        1.  **What does the user want?** Is it about:
             - Finding a restaurant?
             - Booking a table?
             - If YES to either, go to step 2. If NO, say: "I can help you find restaurants or book tables. What would you like to do?"
        2.  **Do you have enough information to use a tool?**
             - If YES, go to step 3.
             - If NO, ask ONE question to get more information. Then go to step 3.
        3.  **Which tool is needed?**
             - If finding a restaurant, use the "search restaurant" tool.


        EXAMPLE CONVERSATION:

        Example 1:
        
        User: Find me a romantic Italian restaurant.

        *uses search_restaurant tool*

        FoodieBot: I found 1 romantic Italian restaurant:
            - La Luna: Known for its romantic ambiance and Italian cuisine.
        
        
        Example 2:

        User: Are there any Cheap Chinese restaurants?

        *uses search_restaurant tool*

        FoodieBot: I found 3 cheap Chinese restaurants:
        - China Garden: Known for its affordable prices and authentic Chinese cuisine.
        - Golden Dragon: Known for its budget-friendly prices and delicious Chinese dishes.
        - Panda Express: Known for its low prices and fast Chinese food.

        Example 3:

        User: Hey what's up?

        FoodieBot: Welcome to FoodieBot! I can help you find restaurants or book tables. What would you like to do?

        User: Tell me a joke.

        FoodieBot: I ain't design to do that buddy!, I can help you find restaurants or book tables and all...


        YOUR TURN:

        """
        

    def _update_conversation_history(self, role: str, content: str) -> None:
        self.conversation_history.append(Message(role=role, content=content))
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY:]

    async def run(self,user_input:str) -> Dict[str,Any]:
        try:
            if not user_input.strip():
                return {"error":"Empty input received"}
            
            self._update_conversation_history("user",user_input)
            return await self._process_query()
    
        except Exception as e:
            return {"error":str(e)}
        
    async def _process_query(self) -> Dict[str,Any]:
        messages = [
            {"role":"system","content":self._get_system_prompt()},
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
                        function_name,function_arguments
                    )
                    messages.append({
                        "tool_call_id":tool_call.id,
                        "role":"tool",
                        "name":function_name,
                        "content":str(tool_result)
                    })

            else:
                messages.append({"role":"assistant","content":response_message.content})
                self._update_conversation_history("assistant",response_message.content)
                break

        return {"messages":response_message.content}
    

    async def _execute_tool(self,function_name:str,function_arguments:Dict[str,Any]) -> Any:
        try:
            for tool in self.tools:
                if tool.name == function_name:
                    result = await tool.agent.process_query(function_arguments)
                    return result 
        except Exception as e:
            raise e

        
async def test_agent_in_terminal():
    """Terminal-based testing interface for the RestaurantAgent"""
    agent = Router()
    print("\nWelcome to FoodieSpot Restaurant Assistant!")
    print("Type 'exit' to quit the conversation.\n")

    try:
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("\nGoodbye!")
                break
                
            response = await agent.run(user_input)
            
            print(f"\nAssistant: {response.get('messages','Nothing to parse')}")
                
    except KeyboardInterrupt:

        print("\n\nConversation terminated by user.")
    


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_in_terminal())