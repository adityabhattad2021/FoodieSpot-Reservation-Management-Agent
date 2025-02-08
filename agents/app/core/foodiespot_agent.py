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

class AgentState(Enum):

    # level 0
    INIT = "init"

    # level 1
    CLASSIFY_USER_INTENT = "classify_user_intent"

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
    required_info: List[str] = []
    selected_tool: Optional[str] = None
    tool_result: Optional[Any] = None
    conversation_history: List[Message] = []

class IntentClassifier:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.available_intents = []

    def classify_intent(self, current_state:AgentState,user_input:str) -> str:
        if current_state == AgentState.CLASSIFY_USER_INTENT:
            self.available_intents = ["FIND_RESTAURANT","OTHER"]
        if current_state == AgentState.FIND_RESTAURANT:
            self.available_intents = ["MAKE_RESERVATION","OTHER"]

        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": user_input}
        ]
        
        response = self.llm_client.chat.completions.create(
            model=settings.DEFAULT_MODEL,
            messages=messages,
            temperature=1,
            max_completion_tokens=100,
            top_p=1,
            stream=True,
            stop=None,
        )

        return json.loads(response.choices[0].message.content).get("categry","OTHER")

    
    def _get_system_prompt(self):
        if self.available_intents == []:
            raise ValueError("No available intents to classify.")
        return f"""
        Classify the user's intent into ONE of these categories, **remembering any information that may have been provided in previous messages**. If the user's intent does not match any of the categories, classify it as "OTHER":
        - {', '.join(self.available_intents)}

        Respond with ONLY the category name in the following JSON format:
        e.g.
        ```json
        {
          "category": {self.available_intents[0]}
        }
        ```

        Few-shot examples:

        User: "I'm craving some Indian food."
        ```json
        {
          "category": "FIND_RESTAURANT"
        }
        ```

        User: "Can you reserve a table for four at the new Italian place on Main Street for Saturday night?"
        ```json
        {
          "category": "MAKE_RESERVATION"
        }
        ```

        User: "What's the capital of France?"
        ```json
        {
          "category": "OTHER"
        }
        ```
        """
    
class FoodieSpotAgent:
    def __init__(self):
        self.llm_client = Groq(api_key=settings.GROQ_API_KEY)
        self.tools = self._initialize_agent_tools()
        self.context = AgentContext(current_state=AgentState.INIT)
        
        # Initialize components
        self.intent_classifier = IntentClassifier(self.llm_client)
        self.information_gatherer = MissingInformationGatherer(self.llm_client)
        self.response_generator = ResponseGenerator(self.llm_client)
        
    def run(self, user_input: str) -> Dict[str, Any]:
        try:
            self.context.conversation_history.append(Message(role="user", content=user_input))
            if self.context.current_state == AgentState.INIT:
                self.context.current_state = AgentState.CLASSIFY_USER_INTENT
                self.context.user_intent = self.intent_classifier.classify_intent(self.context.current_state, user_input)

                if self.context.user_intent == "OTHER":
                    other_intent_messages = [  
                        "I'm still learning, and my specialty is helping with restaurants! I can find restaurants based on cuisine, price, and location, or even help you book a table. Is there anything restaurant-related I can assist you with today?",
                        "Thanks for your message! I'm designed to be a restaurant expert. If you're looking for recommendations or reservations, I'd be happy to help. Otherwise, I might not be the best resource.",
                        "I'm a restaurant bot in training! I'm still working on expanding my skills, but I'm already great at finding restaurants and taking reservations. Let me know if you need help with anything in the culinary world!",
                        "I'm here to help with all your restaurant needs – from finding the perfect spot to booking a table. What kind of restaurant are you in the mood for today?",
                        "Thanks for your message! I'm always learning how to be more helpful. While I'm currently focused on restaurant recommendations and reservations, your input helps me improve. If you'd like to tell me what you were trying to do, it can help me in the future."
                    ]
                    ai_response = random.choice(other_intent_messages)
                    self.context.conversation_history.append(Message(role="assitant", content=ai_response))
                    return {"message": random.choice(other_intent_messages)}
                
                if self.context.user_intent == "FIND_RESTAURANT":
                    self.context.current_state = AgentState.FIND_RESTAURANT


        except Exception as e:
            logging.error(e)
            return {"error": str(e)}

    def _initialize_agent_tools(self):
        self.tools = [SearchRestaurantsTool()]

    def clear(self):
        self.context = AgentContext(current_state=AgentState.INIT)
        logging.info("Agent context cleared.")