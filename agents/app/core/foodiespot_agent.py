import json
import random
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .utils.llm_client import LLMClient
from .utils.prompts import find_restaurant_prompt, intent_classifier_prompt, similarity_search_filter_prompt, reservation_details_extraction_prompt, missing_reservation_details_prompt, handle_reservation_error_prompt
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

class IntentClassifier:
    """
    IntentClassifier classifies the user's intent based on the current state of the agent and the conversation history.
    """
    def __init__(self, llm_client):
        self.llm_client:LLMClient = llm_client

    def classify_intent(self, conversation_history:List[Dict[str,str]]) -> str:
        try:
            messages = [
                {"role": "system", "content": intent_classifier_prompt},
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
        self.reservation_complete:bool = False
        self.reservation_details = ReservationDetails()

    def extract_reservation_details(self, coversation_history:List[Dict[str,str]]):
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
                if hasattr(self.reservation_details,key):
                    setattr(self.reservation_details,key,response[key])
        except Exception as e:
            print("Error in MakeReservation.extract_reservation_details():",e)

    def make_reservation_ec(self,always_success) -> str:
        """
        Simulates a reservation attempt that randomly succeeds or fails with various error cases.
        Returns a JSON string with the result that your AI agent can parse and handle.
        EC - Edge Cases
        """
        restaurant = self.reservation_details.restaurant_name
        date = self.reservation_details.date
        time = self.reservation_details.time
        party_size = self.reservation_details.party_size
        user_id = self.reservation_details.user_id
        
        response_types = [
            # Success case (10% probability)
            {"type": "success", "probability": 0.1},
            
            # Error cases (60% combined probability)
            {"type": "restaurant_full", "probability": 0.2},
            {"type": "restaurant_closed", "probability": 0.2},
            {"type": "invalid_time", "probability": 0.2},
            {"type": "large_party", "probability": 0.1},
            {"type": "system_error", "probability": 0.1},
            {"type": "holiday_policy", "probability": 0.1}
        ]
        
        rand = random.random()
        cumulative_prob = 0
        chosen_type = "success"  
        
        for response in response_types:
            cumulative_prob += response["probability"]
            if rand <= cumulative_prob:
                chosen_type = response["type"]
                break
        
        if always_success:
            chosen_type = "success"
        
        response_data = {
            "status": "success" if chosen_type == "success" else "error",
            "type": chosen_type,
            "restaurant": restaurant,
            "date": date,
            "time": time,
            "party_size": party_size,
            "user_id": user_id
        }
        
        if chosen_type == "success":
            code = ''.join(random.choices('0123456789', k=6))
            response_data.update({
                "message": f"Your reservation at {restaurant} for {party_size} people on {date} at {time} has been confirmed.",
                "reservation_code": code,
            })
        
        elif chosen_type == "restaurant_full":
            response_data.update({
                "message": f"Sorry, {restaurant} is fully booked for {date} at {time}, can you try some other time?",
                "error_code": "RESTAURANT_FULL",
            })
        
        elif chosen_type == "restaurant_closed":
            response_data.update({
                "message": f"{restaurant} is closed on {date}.",
                "error_code": "RESTAURANT_CLOSED",
            })
        
        elif chosen_type == "invalid_time":
            response_data.update({
                "message": f"The requested time {time} is outside {restaurant}'s operating hours.",
                "error_code": "INVALID_TIME",
                "operating_hours": {
                    "open": "11:00 AM",
                    "close": "10:00 PM"
                }
            })
        
        elif chosen_type == "large_party":
            response_data.update({
                "message": f"For parties of {party_size} or more, {restaurant} requires a special reservation process. Please call the restaurant directly.",
                "error_code": "LARGE_PARTY",
                "max_regular_party_size": party_size - 1,
                "contact_phone": "555-123-4567"
            })
        
        elif chosen_type == "system_error":
            response_data.update({
                "message": "A system error occurred while processing your reservation.",
                "error_code": "SYSTEM_ERROR",
                "retry_after": 60 
            })
        
        elif chosen_type == "holiday_policy":
            response_data.update({
                "message": f"Since your reservation is on {date}, which is a holiday, {restaurant} requires a deposit.",
                "error_code": "HOLIDAY_POLICY",
                "deposit_required": True,
                "deposit_amount": 25 * party_size,
                "deposit_currency": "USD"
            })
        
        return json.dumps(response_data)
         
    def generate_reservation_code(self):
        return ''.join(random.choices('0123456789', k=6))

    def handle_messages(self, coversation_history:List[Dict[str,str]]):
        try:
            self.extract_reservation_details(coversation_history)
            print(self.reservation_details)
            missing_fields = self.reservation_details.missing_fields()
            if len(missing_fields) != 0:
                first_field = missing_fields[0]
                system_prompt = missing_reservation_details_prompt + f"Missing field: {first_field}"
                messages = [
                    {"role": "system", "content": system_prompt },
                    *coversation_history
                ]
                response = self.llm_client.get_response(messages,is_json=False)
                return response
            else:
                response = self.make_reservation_ec(always_success=True)
                response = json.loads(response)
                if response["status"] == "success":
                    self.reservation_complete = True
                    self.reservation_details = ReservationDetails()
                    return f"{response['message']} Please show this code at the counter: {response['reservation_code']}."
                else:
                    messages = [
                        {"role": "system", "content": handle_reservation_error_prompt},
                        {"role": "user", "content": json.dumps(response) },
                    ]
                    response = self.llm_client.get_response(messages,is_json=False)
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
            self.context.user_intent = self.intent_classifier.classify_intent(self.context.conversation_history)
            self.context.current_state = self.get_next_state(self.context.user_intent)

            if self.context.current_state == AgentState.FIND_RESTAURANT:
                response = self.find_restaurant.handle_messages(self.context.conversation_history)
                self.context.conversation_history.append({"role":"assistant", "content":response})
                return {"message": response}

            elif self.context.current_state == AgentState.MAKE_RESERVATION:
                response = self.make_reservation.handle_messages(self.context.conversation_history)
                self.context.conversation_history.append({"role": "assistant", "content": response})
                return {"message": response}

            elif self.context.current_state == AgentState.OTHER:
                other_intent_messages = [  
                    "I'm still learning, and my specialty is helping with restaurants! I can find restaurants based on cuisine, price, and location, or even help you book a table. Is there anything restaurant-related I can assist you with today?",
                    "Thanks for your message! I'm designed to be a restaurant expert. If you're looking for recommendations or reservations, I'd be happy to help. Otherwise, I might not be the best resource.",
                    "I'm a restaurant bot in training! I'm still working on expanding my skills, but I'm already great at finding restaurants and taking reservations. Let me know if you need help with anything in the culinary world!",
                    "I'm here to help with all your restaurant needs – from finding the perfect spot to booking a table. What kind of restaurant are you in the mood for today?",
                    "Thanks for your message! I'm always learning how to be more helpful. While I'm currently focused on restaurant recommendations and reservations, your input helps me improve. If you'd like to tell me what you were trying to do, it can help me in the future."
                ]
                response = random.choice(other_intent_messages)
                self.context.conversation_history.append({'role':'assistant', 'content':response})
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