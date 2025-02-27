import random
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .utils.llm_client import LLMClient
from .utils.prompts import find_restaurant_prompt, intent_classifier_prompt, similarity_search_filter_prompt, reservation_details_extraction_prompt, missing_reservation_details_prompt
from .vector_store import search_restaurants,format_search_results_for_llm

class AgentState(Enum):
    # level 1
    GREETING = "greeting"
    # level 2
    FIND_RESTAURANT = "find_restaurant"
    # level 3
    MAKE_RESERVATION = "make_reservation"
    # level x
    OTHER = "other"

class ReservationDetails(BaseModel):
    """
    ReservationDetails stores the details of a reservation.
    """
    restaurant_name: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    party_size: Optional[int] = None
    has_user_confirmed: Optional[bool] = None
    user_id: Optional[str] = '1'

    def missing_fields(self):
        """
        Returns a list of missing fields in the reservation details.
        """

        missing = []
        if not self.restaurant_name:
            missing.append("restaurant_name")
        if not self.date:
            missing.append("date")
        if not self.time:
            missing.append("time")
        if not self.party_size:
            missing.append("party_size")
        if not self.has_user_confirmed or self.has_user_confirmed == False:
            missing.append("has_user_confirmed")
        return missing


class AgentContext(BaseModel):
    """
    AgentContext stores the current state of the agent, the user's intent, and the conversation history.
    """
    current_state: AgentState
    user_intent: Optional[str] = None
    conversation_history: List[Dict[str,str]] = []
    reservation_details: ReservationDetails = ReservationDetails()

class IntentClassifier:
    """
    IntentClassifier classifies the user's intent based on the current state of the agent and the conversation history.
    """
    def __init__(self, llm_client):
        self.llm_client:LLMClient = llm_client

    def classify_intent(self, current_state:AgentState,conversation_history:List[Dict[str,str]]) -> str:
        try:
            if current_state == AgentState.GREETING:
                self.available_intents = ["FIND_RESTAURANT","OTHER"]
            if current_state == AgentState.FIND_RESTAURANT:
                self.available_intents = ["MAKE_RESERVATION", "FIND_RESTAURANT", "OTHER"]
            if current_state == AgentState.MAKE_RESERVATION:
                self.available_intents = ["MAKE_RESERVATION", "FIND_RESTAURANT", "OTHER"]
            system_prompt = intent_classifier_prompt(self.available_intents)
            messages = [
                {"role": "system", "content": system_prompt},
                *conversation_history
            ]
            response = self.llm_client.get_response(messages)
            return response.get("category","OTHER")
        except Exception as e:
            print("Error in IntentClassifier.classify_intent():",e)
            return "OTHER"

class FindRestaurant:
    """
    FindRestaurant class handles the conversation flow for finding restaurants based on user input.
    """
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.system_prompt = find_restaurant_prompt
        self.coversation_history = [
            {"role":"system", "content":find_restaurant_prompt}
        ]

    def _search_and_format_for_llm(self,query, filter_dict=None, top_k=4):
        """
        This function searches for restaurants based on the user query in the vector database and formats the search results for the LLM
        """
        results = search_restaurants(query, filter_dict, top_k)
        context = format_search_results_for_llm(results)
        return context
    
    def similarity_search_filter(self,conversation_history:List[Dict[str,str]]):
        """
        This function prompts the LLM to extract the keywords from the conversation history that describe the user's intent.
        """
        try:
            messages = [
                {"role": "system", "content": similarity_search_filter_prompt},
            ]
            conversation = "Here is the conversation between the user and the assistant:\n"
            for message in conversation_history:
                conversation += f"{message['role']}: {message['content']}\n"
            conversation += "Based on the conversation, what are the keywords that describe the user what the user is talking about?"
            messages.append({"role":"user","content":conversation})
            response = self.llm_client.get_response(messages,is_json=False)
            return response
        except Exception as e:
            print("Error in FindRestaurant.similarity_search_filter():",e)
            return "None"

    
    def handle_messages(self, coversation_history:List[Dict[str,str]]):
        try:
            keywords = self.similarity_search_filter(coversation_history)
            results = self._search_and_format_for_llm(keywords)
            system_pompt_with_context = self.system_prompt + results
            messages = [
                {"role": "system", "content": system_pompt_with_context},
                *coversation_history
            ]
            response = self.llm_client.get_response(messages,is_json=False)
            return response
        except Exception as e:
            print("Error in FindRestaurant.handle_messages():",e)
            return "I'm sorry, I'm having trouble understanding you right now. Please try again."

class MakeReservation:

    def __init__(self, llm_client):
        self.llm_client = llm_client


    def extract_reservation_details(self, coversation_history:List[Dict[str,str]], reservation_details:ReservationDetails):
        try:
            messages = [
                {"role": "system", "content": reservation_details_extraction_prompt},
            ]
            conversation = "Here is the conversation between the user and the assistant:\n"
            for message in coversation_history:
                conversation += f"{message['role']}: {message['content']}\n"
            conversation += "Based on the conversation, please extract the reservation details."
            messages.append({"role":"user","content":conversation})
            response = self.llm_client.get_response(messages,is_json=True)
            for key in response:
                if hasattr(reservation_details,key):
                    setattr(reservation_details,key,response[key])
        except Exception as e:
            print("Error in MakeReservation.extract_reservation_details():",e)

    def make_reservation(self, reservation_details:ReservationDetails):
        """
            This will make the reservation and generate a random code that user can show at the restaurant.
        """
        code = self.generate_reservation_code()
        # Make a call to the backend.

        return f"Your reservation at {reservation_details.restaurant_name} for {reservation_details.party_size} people on {reservation_details.date} at {reservation_details.time} has been confirmed. Please show this code at the restaurant: {code}"
    
    def generate_reservation_code(self):
        return ''.join(random.choices('0123456789', k=6))

    def handle_messages(self, coversation_history:List[Dict[str,str]], reservation_details:ReservationDetails):
        try:
            self.extract_reservation_details(coversation_history,reservation_details)
            print(reservation_details)
            missing_fields = reservation_details.missing_fields()
            if missing_fields:
                first_field = missing_fields[0]
                system_prompt = missing_reservation_details_prompt + f"Missing field: {first_field}"
                messages = [
                    {"role": "system", "content": system_prompt },
                    *coversation_history
                ]
                response = self.llm_client.get_response(messages,is_json=False)
                return response
            else:
                response = self.make_reservation(reservation_details)
                return response
        except Exception as e:
            print("Error in MakeReservation.handle_messages():",e)
            return "I'm sorry, I'm having trouble understanding you right now. Please try again."        

class FoodieSpotAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.context = AgentContext(current_state=AgentState.GREETING)

        self.intent_classifier = IntentClassifier(self.llm_client)
        self.find_restaurant = FindRestaurant(self.llm_client)
        self.make_reservation = MakeReservation(self.llm_client)

    async def run(self, user_input: str) -> Dict[str, Any]:
        try:
            self.context.conversation_history.append({"role":"user", "content":user_input})

            # Classify the user intent for all the messages
            self.context.user_intent = self.intent_classifier.classify_intent(self.context.current_state, self.context.conversation_history)

            if self.context.current_state == AgentState.GREETING:
                self.context.current_state = self.get_next_state(self.context.user_intent)

            if self.context.current_state == AgentState.FIND_RESTAURANT:
                if self.context.user_intent == "FIND_RESTAURANT":
                    response = self.find_restaurant.handle_messages(self.context.conversation_history)
                    self.context.conversation_history.append({"role":"assistant", "content":response})
                    return {"message": response}

                elif self.context.user_intent == "MAKE_RESERVATION":
                    response = self.make_reservation.handle_messages(self.context.conversation_history,self.context.reservation_details)
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
            return AgentState.MAKE_RESERVATION
        elif user_intent == "OTHER":
            return AgentState.OTHER
        else:
            return AgentState.GREETING   

    def clear(self):
        self.context = AgentContext(current_state=AgentState.GREETING)