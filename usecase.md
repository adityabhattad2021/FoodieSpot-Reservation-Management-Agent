# Use case Documentation for FoodieSpot Conversational AI Agent

## Goal
**Long Term Goal**  
Transform restaurant discovery and reservation management into a seamless, personalized experience across all FoodieSpot locations through intelligent conversational AI Agent.

**Success Criteria**   
- ~30-50% reduction in customer service calls for reservations
- User satisfaction rate for bot interactions > 80%
- Average conversation completion rate > 85%

## Use Case 
FoodieBot helps diners find ideal restaurants from 50+ locations based on cuisine preferences, party size, and ambiance. The AI agent analyzes real-time table availability, suggests personalized options with menus, handles complex modifications ("Change from 4 to 6 people at 8PM"), and confirms reservations. It understands and remember user preferences for repeat visits.

## Key Steps (End User Flow)
1. **Greeting**  
   "Hello! I'm your FoodieSpot assistant. How can I help you today?"

2. **Preference Capture**  
   - Natural language understanding for:  
     `Cuisine type → "Something with good vegan options"`  
     `Location constraints → "Near Central Station"`  
     `Special requests → "Quiet area for business meeting"`

3. **Smart Filtering**  
   Presents 3 options with:  
   - Real-time table availability check  
   - Menu highlights matching dietary needs  

4. **Conversational Reservation**  
   Handles complex modifications:  
   "Actually, make it 30 minutes later" → auto-checks system

5. **Confirmation & Integration**  (Not implemented in the prototype)
   Sends SMS + calendar invite with:  
   - Dynamic Google Maps link  
   - Chef's recommendation pre-order option

## State Transition Diagram  
![State Transition Diagram](https://github.com/user-attachments/assets/f938160d-8f77-4060-8599-1f4c65d02177)
  
## Bot Features  
| Feature | Specification | Difficulty | Notes |
|---------|---------------|------------|-------|
| Dynamic Intent Recognition | Tool calling with Llama-3.1-8b for 5 intents (search, booking, modify, menu req, raise to support staff) | Red | Cannot handle yet "I want to push my 7PM booking by half hour" → detect modify intent |
| Contextual Memory | Stores user preferences/booking history in database | Green | Feature Suggestion |
| Use user location for better contextulized restaurant suggestions | Get the user location, and use google map api to find distance from the restaurant and feed the data as context to the LLM | Yellow | Feature suggestion |


**Key Tools Required**  
- Restaurant Reservation Management API Access
- LLM API access 

## Scale-up Strategy  
1. **Pilot Phase**   
   - Test with ~50-100 loyalty members  
   - Collect verbatim feedback through "How did we do?" prompt popup at the end of conversation with the agent

2. **Suggested Upgrades**
   - Implement voice-based interaction for hands-free reservations
   - Implement a feedback system for user to rate the bot's performance
   - Use an LLM which is good with different accents and languages

2. **Enterprise Integration**  
   - Connect to POS systems for prepayments  
   - Add staff notification system for special requests

## Key Challenges/Limitations & Solutions  
1. **Dynamic Intent Handling**  
   *Challenge*: Llama-3's tool calling consistency for complex requests  
   *Solution*: Use better LLM for router agent and implement tier fallback with human handoff  

2. **Personalization at Scale**  
   *Challenge*: Maintaining context across long conversations  
   *Solution*: 1. Use sliding window approach for context management
	       2. Implement priority-based context pruning
               3. Create a user profile model and store user preferences and history separately from conversation context

**Assumptions**  
- Currently supports english language only.

