import logging
import json

from groq import Groq
from pydantic import BaseModel
from typing import List, Dict, Any
from agents.core.config import settings
from agents.core.specialized.search_agent import SearchAgent
from agents.core.specialized.create_custome import CreateCustomerAgent
from agents.core.specialized.get_customer_by_email import GetCustomerByEmailAgent
from agents.core.specialized.get_customer_by_phone import GetCustomerByPhoneAgent
from agents.core.specialized.get_restraurant_table import GetRestraurantTablesAgent
from agents.core.specialized.create_reservation import CreateReservationAgent

MAX_CONVERSATION_HISTORY = 10
MAX_ITERATIONS = 2

logging.basicConfig(
    level=logging.WARNING,  # Set the desired log level
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",

)


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
        logging.debug("Router initialized.")
        
    def _initialize_agent_tools(self) -> List[AgentTool]:
        tools = [
            AgentTool("search_restraurant", SearchAgent()),
            AgentTool("get_table_information", GetRestraurantTablesAgent()),
            AgentTool("create_new_customer", CreateCustomerAgent()),
            AgentTool("get_customer_by_email", GetCustomerByEmailAgent()),
            AgentTool("get_customer_by_phone", GetCustomerByPhoneAgent()),
            AgentTool("create_reservation", CreateReservationAgent())
        ]
        logging.debug(f"Agent tools initialized: {[tool.name for tool in tools]}")
        return tools

    def _get_system_prompt(self) -> str:
        return """
        You are FoodieBot. Your job is to understand what the user wants and use the *best* tool to help with restaurants. If it's not about restaurants, tell them what you can do.

        **TOOLS:**

        *   **search_restaurant:** Use this to search for restaurants based on cuisine, price, etc).
        *   **get_table_information:** Use this to get information about restaurant tables.
        *   **create_new_customer:** Use this to create a new customer account.
        *   **get_customer_by_email:** Use this to find a customer by email.
        *   **get_customer_by_phone:** Use this to find a customer by phone.
        *   **create_reservation:** Use this to create a reservation.

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
        4.  **If tool responds with more information needed or error:**
             - Ask the user for more information.
             - Try calling the tool with the new information and correct imformation.
        5.  **If tool responds with success:**
             - Present the information to the user.
             - Ask if user wants to do anything else.


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

        User: are there any tables available at La Luna for 2 people?

        *uses get_table_information tool* 

        Example 3:

        User: Hey what's up?

        FoodieBot: Welcome to FoodieBot! I can help you find restaurants or book tables. What would you like to do?

        User: Tell me a joke.

        FoodieBot: I ain't design to do that buddy!, I can help you find restaurants or book tables and all...

        YOUR TURN:

        """
        

    def _update_conversation_history(self, role: str, content: str) -> None:
        self.conversation_history.append(Message(role=role, content=content))
        logging.debug(f"Conversation history updated: {content}")
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY:]
            logging.debug("Conversation history trimmed.")

    async def run(self,user_input:str) -> Dict[str,Any]:
        try:
            logging.info(f"Received user input: {user_input}")
            if not user_input.strip():
                logging.warning("Empty input received.")
                return {"error":"Empty input received"}
            
            self._update_conversation_history("user",user_input)
            result = await self._process_query()
            logging.info(f"Query processed. Result: {result}")
            return result
    
        except Exception as e:
            logging.exception("Error during run method:")
            return {"error":str(e)}
        
    async def _process_query(self) -> Dict[str,Any]:
        messages = [
            {"role":"system","content":self._get_system_prompt()},
            *[msg.model_dump() for msg in self.conversation_history]
        ]

        logging.debug(f"Initial messages sent to LLM: {messages}")

        for i in range(MAX_ITERATIONS):

            logging.info(f"Starting iteration {i+1}/{MAX_ITERATIONS}")

            response = self.llm_client.chat.completions.create(
                model=settings.DEFAULT_MODEL,
                messages=messages,
                max_tokens=4096,
                tools=[tool.to_dict() for tool in self.tools],
                tool_choice="auto",
            )

            logging.debug(f"LLM API response: {response}")

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            print(response_message)

            if tool_calls:
                logging.info(f"Tool calls detected: {tool_calls}")

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

                logging.debug(f"Messages updated with tool calls: {messages}")

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_arguments = tool_call.function.arguments

                    logging.info(f"Executing tool: {function_name} with arguments: {function_arguments}")

                    tool_result = await self._execute_tool(
                        function_name,function_arguments
                    )

                    logging.info(f"Tool execution result: {tool_result}")
                    messages.append({
                        "tool_call_id":tool_call.id,
                        "role":"tool",
                        "name":function_name,
                        "content":str(tool_result)
                    })

                    logging.debug(f"Messages updated with tool result: {messages}")

            else:
                logging.info("No tool calls detected.")
                messages.append({"role":"assistant","content":response_message.content})
                self._update_conversation_history("assistant",response_message.content)
                logging.debug(f"Messages updated with assistant content: {response_message.content}")
                break

        logging.info("Processing query completed.")
        return {"messages":response_message.content}
    

    async def _execute_tool(self,function_name:str,function_arguments:Dict[str,Any]) -> Any:
        logging.info(f"Executing tool: {function_name} with arguments: {json.dumps(function_arguments)}")
        try:
            for tool in self.tools:
                if tool.name == function_name:
                    print("Tool found")
                    logging.debug(f"Found matching tool: {tool.name}")
                    result = await tool.agent.process_query(function_arguments)
                    logging.info(f"Tool {function_name} executed successfully. Result: {result}")
                    print("Tool executed successfully",result)
                    return result 
        except Exception as e:
            logging.exception(f"Error executing tool {function_name}:")
            return {"error":str(e)}

        
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