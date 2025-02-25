import os
import logging
import json
import random
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from groq import Groq
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from ..config import settings
from .tools.restaurant_management import SearchRestaurantsTool

class LLMClient:
    def __init__(self):
        self.llm = Groq(api_key=settings.GROQ_API_KEY)

    def get_response(self, messages: List[Dict[str, str]],is_json=True):
        try:
            response_format = None
            if is_json:
                response_format = {"type": "json_object"}
            response = self.llm.chat.completions.create(
                model=settings.DEFAULT_MODEL,
                messages=messages,
                temperature=1,
                max_completion_tokens=100,
                top_p=1,
                stream=False,
                response_format=response_format,
                stop=None,
            )
            if is_json:
                return json.loads(response.choices[0].message.content)
            else:
                return response.choices[0].message.content
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

class AgentContext(BaseModel):
    current_state: AgentState
    user_intent: Optional[str] = None
    conversation_history: List[Dict[str,str]] = []

class IntentClassifier:
    def __init__(self, llm_client):
        self.llm_client:LLMClient = llm_client
        self.available_intents = []

    def classify_intent(self, current_state:AgentState,conversation_history:List[Dict[str,str]]) -> str:
        if current_state == AgentState.GREETING:
            self.available_intents = ["FIND_RESTAURANT","OTHER"]
        if current_state == AgentState.FIND_RESTAURANT:
            self.available_intents = ["MAKE_RESERVATION","OTHER","FIND_RESTAURANT"]

        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            *conversation_history
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

class FindRestaurant:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.system_prompt = self._get_system_prompt()
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.coversation_history = [
            {"role":"system", "content":self.system_prompt}
        ]
        index_name = "restaurant-search"
        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
        self.index = self.pc.Index(index_name)

    def _search_restaurants(self,query,filter_dict=None,top_k=5):
        query_embedding = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[query],
            parameters={"input_type": "query"}
        )

        results = self.index.query(
            namespace="restaurants",
            vector=query_embedding[0]["values"],
            filter=filter_dict,
            top_k=top_k,
            include_metadata=True
        )

        return results
    
    def _format_search_results_for_llm(self,results):
        if not results or "matches" not in results or not results["matches"]:
            return "No restaurants found matching your criteria."
        formatted_context = "RESTAURANT SEARCH RESULTS:\n\n"
        for i, match in enumerate(results["matches"], 1):
            restaurant = match["metadata"]
            similarity_score = match["score"]
            formatted_context += f"RESTAURANT #{i} (Relevance Score: {similarity_score:.2f})\n"
            formatted_context += f"Name: {restaurant['name']}\n"
            formatted_context += f"Cuisine: {restaurant['cuisine']}\n"
            formatted_context += f"Location: {restaurant['area']}\n"
            formatted_context += f"Price Range: {restaurant['price_range']}\n"
            formatted_context += f"Ambiance: {restaurant['ambiance']}\n"
            formatted_context += f"Description: {restaurant['description']}\n"
            formatted_context += f"Specialties: {restaurant['specialties']}\n"
            formatted_context += f"Dietary Options: {restaurant['dietary_options']}\n"
            formatted_context += f"Features: {restaurant['features']}\n\n"
        return formatted_context

    def _search_and_format_for_llm(self,query, filter_dict=None, top_k=5):
        results = self._search_restaurants(query, filter_dict, top_k)
        context = self._format_search_results_for_llm(results)
        return f"{context}\n\nUser message: {query}"
    
    def _get_system_prompt(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "system_prompts.json")
        with open(file_path) as f:
            prompts = json.load(f)
        return prompts.get("find_restaurant_system_prompt")
    
    def handle_messages(self, user_input: str):
        formatted_query = self._search_and_format_for_llm(user_input)
        self.coversation_history.append({"role":"user", "content":formatted_query})
        response = self.llm_client.get_response(self.coversation_history,is_json=False)
        self.coversation_history.append({"role":"assistant", "content":response})
        return response

class FoodieSpotAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.tools = self._initialize_agent_tools()
        self.context = AgentContext(current_state=AgentState.GREETING)

        self.intent_classifier = IntentClassifier(self.llm_client)
        self.find_restaurant = FindRestaurant(self.llm_client)

    async def run(self, user_input: str) -> Dict[str, Any]:
        try:
            self.context.conversation_history.append({"role":"user", "content":user_input})
            self.context.user_intent = self.intent_classifier.classify_intent(self.context.current_state, self.context.conversation_history)
            print("User intent:", self.context.user_intent)
            
            if self.context.current_state == AgentState.GREETING:
                self.context.current_state = self.get_next_state(self.context.user_intent)

            if self.context.current_state == AgentState.FIND_RESTAURANT:
                if self.context.user_intent == "FIND_RESTAURANT":
                    response = self.find_restaurant.handle_messages(user_input)
                    self.context.conversation_history.append({"role":"assistant", "content":response})
                    return {"message": response}

                elif self.context.user_intent == "MAKE_RESERVATION":
                    response = "I'd be happy to help you make a reservation. This feature is coming soon!"
                    self.context.conversation_history.append({"role": "assistant", "content": response})
                    return {"message": response}
                elif self.context.user_intent == "OTHER":
                    self.context.current_state = AgentState.OTHER

            if self.context.current_state == AgentState.OTHER:
                self.context.current_state = self.get_next_state(self.context.user_intent)
                other_intent_messages = [  
                    "I'm still learning, and my specialty is helping with restaurants! I can find restaurants based on cuisine, price, and location, or even help you book a table. Is there anything restaurant-related I can assist you with today?",
                    "Thanks for your message! I'm designed to be a restaurant expert. If you're looking for recommendations or reservations, I'd be happy to help. Otherwise, I might not be the best resource.",
                    "I'm a restaurant bot in training! I'm still working on expanding my skills, but I'm already great at finding restaurants and taking reservations. Let me know if you need help with anything in the culinary world!",
                    "I'm here to help with all your restaurant needs – from finding the perfect spot to booking a table. What kind of restaurant are you in the mood for today?",
                    "Thanks for your message! I'm always learning how to be more helpful. While I'm currently focused on restaurant recommendations and reservations, your input helps me improve. If you'd like to tell me what you were trying to do, it can help me in the future."
                ]
                response = random.choice(other_intent_messages)
                self.context.conversation_history.append({'role':'assistant', 'content':response})
                self.context.current_state = AgentState.GREETING
                return {"message": response}


        except Exception as e:
            print("Error in agent.run():",e)
            return {"message": "I'm sorry, I'm having trouble understanding you right now. Please try again"}
        
    def get_next_state(self, user_intent):
        if user_intent == "FIND_RESTAURANT":
            return AgentState.FIND_RESTAURANT
        elif user_intent == "MAKE_RESERVATION":
            return AgentState.RESERVATION_IN_PROGRESS 
        elif user_intent == "OTHER":
            return AgentState.OTHER
        else:
            return AgentState.GREETING   

    def _initialize_agent_tools(self):
        return {
            "search_restaurants": SearchRestaurantsTool()
        }

    def clear(self):
        self.context = AgentContext(current_state=AgentState.GREETING)
        self.find_restaurant = FindRestaurant(self.llm_client)