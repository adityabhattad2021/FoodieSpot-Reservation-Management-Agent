import logging
import json
import datetime
import random
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from groq import Groq
from ..config import settings
from .tools.restaurant_management import SearchRestaurantsTool



class LLMClient:
    def __init__(self):
        self.llm = Groq(api_key=settings.GROQ_API_KEY)

    def get_response(self, messages: List[Dict[str, str]]):
        try:
            response = self.llm.chat.completions.create(
                model=settings.DEFAULT_MODEL,
                messages=messages,
                temperature=1,
                max_completion_tokens=100,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}


class AgentState(Enum):
    # level 1
    GREETING = "GREETING"

    # level 2
    FIND_RESTAURANT = "find_restaurant"
    FAQ = "faq"
    MENU = "menu"
    MODIFY_BOOKING = "modify_booking"

    # level 3
    RESERVATION_IN_PROGRESS = "reservation_in_progress"
    MODIFICATION_IN_PROGRESS = "modification_in_progress"

    # level 4
    DATE_SELECTION = "date_selection"

    # level 5
    TIME_SELECTION = "time_selection"

    # level 6
    GUEST_SELECTION = "guest_selection"

    # level 7
    CONFIRMATION = "confirmation"

    # level x
    OTHER = "other"


class Message(BaseModel):
    role: str
    content: str

class AgentContext(BaseModel):
    current_state: AgentState
    user_intent: Optional[str] = None
    conversation_history: List[Message] = []

class IntentClassifier:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.available_intents = []

    def classify_intent(self, current_state:AgentState,user_input:str) -> str:
        if current_state == AgentState.GREETING:
            self.available_intents = ["FIND_RESTAURANT","OTHER"]
        if current_state == AgentState.FIND_RESTAURANT:
            self.available_intents = ["MAKE_RESERVATION","OTHER","FIND_RESTAURANT"]

        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": user_input}
        ]
        
        response = self.llm_client.get_response(messages)

        return response.get("category","OTHER")

    
    def _get_system_prompt(self):
        if self.available_intents == []:
            raise ValueError("No available intents to classify.")
        return f"""
            Classify the user's intent into ONE of these categories, **remembering any information that may have been provided in previous messages**. If the user's intent does not match any of the categories, classify it as "OTHER":
            - {', '.join(self.available_intents)}

            Respond with ONLY the category name in the following JSON format:
            e.g.
            ```json
            {{
            "category": "{self.available_intents[0]}"
            }}
            ```

            Few-shot examples:

            User: "I'm craving some Indian food."
            ```json
            {{
            "category": "FIND_RESTAURANT"
            }}
            ```

            User: "Can you reserve a table for four at the new Italian place on Main Street for Saturday night?"
            ```json
            {{
            "category": "MAKE_RESERVATION"
            }}
            ```

            User: "What's the capital of France?"
            ```json
            {{
            "category": "OTHER"
            }}
            ```
            """
    
class FoodieSpotAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.tools = self._initialize_agent_tools()
        self.context = AgentContext(current_state=AgentState.GREETING)
        
        # Initialize components
        self.intent_classifier = IntentClassifier(self.llm_client)

    async def run(self, user_input: str) -> Dict[str, Any]:
        try:
            self.context.conversation_history.append(Message(role="user", content=user_input))
            self.context.user_intent = self.intent_classifier.classify_intent(self.context.current_state, user_input)
            
            if self.context.current_state == AgentState.GREETING:
                self.context.current_state = self.get_next_state(self.context.user_intent)

            print("Current state:", self.context.current_state)
            print("User intent:", self.context.user_intent)

            if self.context.current_state == AgentState.FIND_RESTAURANT:
                if self.context.user_intent == "FIND_RESTAURANT":

                    # Find a restaurant based on user input
                    response = self.llm_client.get_response(messages=[
                            {
                                "role": "system",
                                "content": "  You are a helpful assistant that can use tools to fulfill user requests.  You have access to the following tool:\n\n        ```json\n        {\n          \"name\": \"search_restaurants\",\n          \"description\": \"Search restaurants with multiple filters.\",\n          \"parameters\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"cuisine_type\": {\n                \"type\": \"string\",\n                \"enum\": [\"North Indian\", \"South Indian\", \"Chinese\", \"Italian\", \"Continental\",\"Mughlai\",\"Thai\",\"Japanese\",\"Mexican\",\"Mediterranean\",\"Bengali\",\"Gujarati\",\"Punjabi\",\"Kerala\",\"Hyderabadi\"],\n                \"description\": \"Type of cuisine\"\n              },\n              \"price_range\": {\n                \"type\": \"string\",\n                \"enum\": [\"$\", \"$$\", \"$$$\", \"$$$$\"],\n                \"description\": \"Price category\"\n              },\n              \"ambiance\": {\n                \"type\": \"string\",\n                \"enum\": [\"Casual\", \"Fine Outdoor\", \"Family\", \"Lounge\"],\n                \"description\": \"Restaurant atmosphere\"\n              },\n              \"min_seating\": {\n                \"type\": \"integer\",\n                \"description\": \"Minimum seating capacity required\"\n              },\n              \"special_event_space\": {\n                \"type\": \"boolean\",\n                \"description\": \"Whether special events can be hosted\"\n              },\n              \"dietary_options\": {\n                \"type\": \"string\",\n                \"description\": \"Specific dietary requirements (e.g., Vegetarian, Vegan, Gluten-free)\"\n              },\n                \"skip\": {\"type\": \"integer\", \"default\": 0, \"description\": \"Number of results to skip\"},\n                \"limit\": {\"type\": \"integer\", \"default\": 100, \"description\": \"Maximum number of results to return\"}\n            },\n            \"required\": []  // No parameters are strictly required\n          }\n        }\n        ```\n\n        To use this tool, respond with a JSON object that conforms to the tool's schema.  Specifically, the JSON should have a \"tool_name\" key and a \"tool_input\" key.  The \"tool_input\" should be a JSON object containing the parameters for the tool.  If the user's request can be fulfilled directly without using the tool, respond directly with the answer."
                            },
                            {
                                "role": "user",
                                "content": "I'm looking for a casual Italian restaurant that's not too expensive."
                            },
                            {
                                "role": "assistant",
                                "content": "{\n          \"tool_name\": \"search_restaurants\",\n          \"tool_input\": {\n            \"cuisine_type\": \"Italian\",\n            \"price_range\": \"$\",\n            \"ambiance\": \"Casual\"\n          }\n }\n"
                            },
                            {
                                "role": "user",
                                "content": "User: I need a place that can host a party for 50 people, serves North Indian food and has a lounge."
                            },
                            {
                                "role": "assistant",
                                "content": "{\n   \"tool_name\": \"search_restaurants\",\n   \"tool_input\": {\n    \"cuisine_type\": \"North Indian\",\n    \"ambiance\": \"Lounge\",\n    \"min_seating\": 50,\n    \"ambiance\": \"Lounge\",\n    \"special_event_space\": true\n  }\n}"
                            },
                            {
                                "role": "user",
                                "content": "I'm looking for a vegan-friendly restaurant."
                            },
                            {
                                "role": "assistant",
                                "content": "{\n   \"tool_name\": \"search_restaurants\",\n   \"tool_input\": {\n     \"dietary_options\": \"Vegan\"\n   }\n}"
                            },
                            {
                                "role": "user",
                                "content": "Suggest a good restaurant in Nagpur"
                            },
                            {
                                "role": "assistant",
                                "content": "{\n   \"tool_name\": \"search_restaurants\",\n   \"tool_input\": {}\n}"
                            },
                            {
                                "role": "user",
                                "content": "Suggest a good restaurant in sadar, nagpur"
                            },
                            {
                                "role": "assistant",
                                "content": "{\n   \"tool_name\": \"search_restaurants\",\n   \"tool_input\": {}\n}"
                            },
                            {
                                "role": "user",
                                "content": "bro koi downtown me accha sa hotel bta na"
                            },
                            {
                                "role": "assistant",
                                "content": "{\n   \"tool_name\": \"search_restaurants\",\n   \"tool_input\": {}\n}"
                            },
                            {
                                "role": "user",
                                "content": user_input
                            }
                        ])

                    selected_tool = response.get("tool_name")
                    tool_input = response.get("tool_input")

                    result = await self.tools[selected_tool].execute(**tool_input)
                    print(result)

                    return {"message": "It is fucking workds!"}


                elif self.context.user_intent == "MAKE_RESERVATION":
                    pass
                elif self.context.user_intent == "OTHER":
                    self.context.current_state = AgentState.OTHER

            if self.context.current_state == AgentState.OTHER:
                print("Atleast we are here...................")
                self.context.current_state = self.get_next_state(self.context.user_intent)
                other_intent_messages = [  
                    "I'm still learning, and my specialty is helping with restaurants! I can find restaurants based on cuisine, price, and location, or even help you book a table. Is there anything restaurant-related I can assist you with today?",
                    "Thanks for your message! I'm designed to be a restaurant expert. If you're looking for recommendations or reservations, I'd be happy to help. Otherwise, I might not be the best resource.",
                    "I'm a restaurant bot in training! I'm still working on expanding my skills, but I'm already great at finding restaurants and taking reservations. Let me know if you need help with anything in the culinary world!",
                    "I'm here to help with all your restaurant needs – from finding the perfect spot to booking a table. What kind of restaurant are you in the mood for today?",
                    "Thanks for your message! I'm always learning how to be more helpful. While I'm currently focused on restaurant recommendations and reservations, your input helps me improve. If you'd like to tell me what you were trying to do, it can help me in the future."
                ]
                ai_response = random.choice(other_intent_messages)
                self.context.conversation_history.append(Message(role="assitant", content=ai_response))
                self.context.current_state = AgentState.GREETING
                return {"message": ai_response}


        except Exception as e:
            return {"error": str(e)}
        
    def get_next_state(self, user_intent):
        if user_intent == "FIND_RESTAURANT":
            return AgentState.FIND_RESTAURANT
        elif user_intent == "MAKE_RESERVATION":
            return AgentState.RESERVATION_IN_PROGRESS  # Or a more specific state
        elif user_intent == "OTHER":
            return AgentState.OTHER
        else:
            return AgentState.GREETING #Default to init
        

    

    def _initialize_agent_tools(self):
        return {
            "search_restaurants": SearchRestaurantsTool()
        }


    def clear(self):
        self.context = AgentContext(current_state=AgentState.GREETING)
        logging.info("Agent context cleared.")