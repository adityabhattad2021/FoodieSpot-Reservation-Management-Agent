import logging
import json
import datetime
from groq import Groq
from pydantic import BaseModel
from typing import List, Dict, Any

from ..config import settings
from .specialized_agent.search_restaurant import SearchAgent
from .specialized_agent.create_customer import CreateCustomerAgent
from .specialized_agent.get_customer_by_email import GetCustomerByEmailAgent
from .specialized_agent.get_customer_by_phone import GetCustomerByPhoneAgent
from .specialized_agent.get_restraurant_table import GetRestraurantTablesAgent
from .specialized_agent.create_reservation import CreateReservationAgent
from .specialized_agent.create_support_ticket import CreateSupportTicketAgent

MAX_CONVERSATION_HISTORY = 10
MAX_ITERATIONS = 2

logging.basicConfig(
    level=logging.WARNING, 
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)

class Message(BaseModel):
    role: str
    content: str


class AgentTool:
    def __init__(self,name:str,description:str,agent:Any):
        self.name = name
        self.description = description
        self.agent = agent

    def to_dict(self) -> Dict[str,Any]:
        return self.agent.to_dict(self.name,self.description)

class RouterAgent:
    def __init__(self):
        self.llm_client = Groq(api_key=settings.GROQ_API_KEY)
        self.tools = self._initialize_agent_tools()
        self.conversation_history: List[Message] = []
        logging.debug("Router initialized.")
        
    def _initialize_agent_tools(self) -> List[AgentTool]:
        tools = [
            AgentTool("search_restraurant","Search for restraurants based on different parameters", SearchAgent()),
            AgentTool("get_table_information","Get table information for the required restraurant, use this before creating a reservation to check available", GetRestraurantTablesAgent()),
            AgentTool("create_new_customer","Use to create new customer" ,CreateCustomerAgent()),
            AgentTool("get_customer_by_email","Find customer details by email", GetCustomerByEmailAgent()),
            AgentTool("get_customer_by_phone","Find customer details by phone", GetCustomerByPhoneAgent()),
            AgentTool("create_reservation","Create reservation at a restarurant for the customer", CreateReservationAgent()),
            AgentTool("create_support_ticket","Connect user to human support when required", CreateSupportTicketAgent())
        ]
        logging.debug(f"Agent tools initialized: {[tool.name for tool in tools]}")
        return tools

    def _get_system_prompt(self) -> str:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
            Current time: {current_time}     

            You are FoodieBot, an expert restaurant concierge AI. FoodieBot's primary functions are:
            1. Restaurant discovery and recommendations
            2. Reservation management
            3. Customer account support  
            4. Use tools to assist users in finding restaurants, making reservations, and managing customer accounts.
            
            You have the following tools at your disposal:
            1. search_restaurant 
            2. create_reservation 
            3. get_table_information 
            4. customer_tools
            5. create_support_ticket
             
            
            ## RULES that foodieBot always follows:  
            1. NEVER make up any restaurant information by yourself, always use the tools when needed.
            2. ALWAYS execute tool with validated parameters.
            
            ## Here is how foodie bot solves an error:
            1. Understands the error message, and if any extra information needed.
            2. Asks the user for missing information.
            3. Tries again with the corrected information.   
            
            ## EXAMPLE CONVERSATION:

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
        
    def clear(self):
        self.conversation_history.clear()
        logging.info("Conversation history cleared.")

        
async def test_agent_in_terminal():
    """Terminal-based testing interface for the RestaurantAgent"""
    agent = RouterAgent()
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