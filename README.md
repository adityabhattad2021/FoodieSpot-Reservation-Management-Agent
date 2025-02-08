# FoodieSpot Restaurant Management System

## 📑 Index
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [Prompt Engineering Techniques](#prompt-engineering-techniques)
6. [Challenges & Known Issues](#challenges-and-known-issues)
7. [Example Conversation](#example-converation)
8. [Use Case Documentation](https://github.com/adityabhattad2021/SarvamAI-Assignment/blob/main/usecase.md)

## Overview
FoodieSpot is an AI-powered restaurant management system designed to streamline the reservation process across multiple restaurant locations. The system features a conversational agent that helps customers find restaurants and make reservations while providing comprehensive management tools for restaurant operators.

### ✨ Key Features
- 🤖 Intelligent restaurant recommendations based on user preferences
- ⚡ Real-time table availability checking
- 📅 Automated reservation management
- 👤 Customer profile management
- 🎫 Support ticket system
- 💬 Conversational AI interface

## Architecture

### Component Overview

The system consists of three main components:

1. **AI Agent Service (`/agents`)**: 
   - FastAPI server providing REST endpoints
   - Conversational AI implementation using Groq API
   - Specialized agents for different tasks

2. **Backend Service (`/backend`)**:
   - FastAPI server with REST endpoints
   - Handles core business logic and data management
   - Database operations and authentication

3. **Frontend (`/frontend`)**:
   - React-based web interface
   - Built with TypeScript and Tailwind CSS
   - Responsive design for all devices
  
### Integration Points
- AI Agent ↔️ Backend Service: REST API
- Frontend ↔️ Backend: REST API
- Frontend ↔️ AI Agent: REST API
- Database ↔️ Backend: SQL/ORM

### Data Flow
![data flow](https://github.com/user-attachments/assets/1f9021a3-cec2-45b4-9fe2-da59b9b47537)

### Sequeunce Diagram
![sequence diagram](https://github.com/user-attachments/assets/22504226-46e7-483c-a1f8-31bafa0b5be6)

## Project Structure
```
.
├── agents/                 # AI Agent Service
│   ├── app/
│   │   ├── config.py      # Configuration settings
│   │   ├── core/          # Core agent functionality
│   │   │   ├── base_agent.py          # Base agent class, inhereted by specialized agents
│   │   │   ├── router.py              # Main router agent that interacts with the end user and specialized agents
│   │   │   ├── specialized_agent/     # Task-specific agents
│   │   │   │   ├── create_customer.py       # Customer creation
│   │   │   │   ├── create_reservation.py    # Reservation handling
│   │   │   │   ├── create_support_ticket.py # Support tickets
│   │   │   │   ├── get_customer_by_email.py # Customer lookup
│   │   │   │   ├── get_restraurant_table.py # Table management
│   │   │   │   └── search_restaurant.py     # Restaurant search
│   │   │   ├── tools/                 # Agent tools
│   │   │   │   ├── base_tool.py            # Base tool class, inherited by specialized tools
│   │   │   │   ├── customer_managment.py   # Tools related to customer operations 
│   │   │   │   ├── reservation_management.py # Tools related to reservation ops
│   │   │   │   └── restaurant_management.py  # Tools related to estaurant ops
│   │   │   └── utils/                 # Utility functions
|   |   |       ├── api_client.py         # API client for interacting with backend (restaurant API)
│   │   └── main.py       # Agent service entry point
│   └── requirements.txt   # Agent dependencies
├── backend/               # Backend Service
│   ├── app/
│   │   ├── auth.py       # Authentication logic
│   │   ├── crud.py       # Database operations
│   │   ├── database.py   # Database configuration
│   │   ├── init_db.py    # Database initialization
│   │   ├── main.py       # Backend entry point
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Data validation schemas
│   │   └── seed.py       # Initial data seeding
│   └── requirements.txt   # Backend dependencies
└── frontend/             # React Frontend
    ├── src/
    │   ├── components/   # Reusable components
    │   ├── pages/        # Application pages
    │   └── context/      # Auth Context for admin dashboard
```

## Setup Instructions

### Prerequisites

Before you begin, ensure you have:
- Docker and Docker Compose installed
- Groq API key

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd foodiespot
   ```

2. **Configure Environment**
   ```bash
   # Copy environment template
   cp .env.example .env

   # Add your Groq API key
   GROQ_API_KEY=your_api_key_here
   ```

3. **Launch Services**
   ```bash
   # Start all services
   docker-compose up --build
   ```

4. **Access the Application**
   - Frontend: [http://localhost:3000](http://localhost:3000) (credentials for admin staff login are in .env.example file)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Agent API Docs: [http://localhost:8001/docs](http://localhost:8001/docs)

5. **Shutdown**
   ```bash
   docker-compose down -v
   ```

## Prompt Engineering Techniques

> Reference: [router.py](agents/app/core/router.py) and [specialized agents](agents/app/core/specialized_agent/create_customer.py)

### Key Design Elements

1. **Role Definition & Scope Enforcement**
   ```python
   "You are FoodieBot. Your job is to understand what the user wants and use the *best* tool to help with restaurants."
   ```
   - Strict scope limitation
   - Explicit restaurant context
   - Tool-oriented thinking

2. **Tool Integration Framework**
   ```python
   "**TOOLS:**\n1. **search_restaurant:** Use this to search..."
   ```
   - Prioritized by usage frequency
   - Natural language descriptions
   - Embedded tool selection logic

3. **Defined Rules**
   ```python
   """1. **What does the user want?** Is it about:
       - Finding a restaurant?
       - Booking a table?"""
   ```
   - Suggests clear decision-making process


4. **Tries to teach agent to handle error and try again**
   ```python
   """4. **If tool responds with more information needed:**
       - Ask the user ONE question
       - Try calling tool with new information"""
   ```
   - Single-question rule prevents loops
   - Tool-based validation

5. **Few Shot Prompting**
   ```python
   "Example 1:\nUser: Find me romantic Italian..."
   ```
   - Demonstrates ideal interactions
   - The specialized agents always work correctly with the given examples

6. **Contextual Awareness**
   ```python
   current_time = datetime.datetime.now().strftime(...)
   f"Current time: {current_time}"
   ```
   - Helps agent to provide time-sensitive responses such as making a reservation after 2 days.

#### Limitations
 - Even with current design, the agent sometimes fails to understand the user intent and provides incorrect response.
 - This can be improved by using a better model for router agent.

## Challenges and Known Issues

### Current Limitations

1. **Conversation Management**
   - In-memory conversation storage ([session_manager.py](agents/app/session_manager.py))
   - Tool parameter accuracy issues
   - Model improvement needed

2. **Authentication**
   - Limited agent service security
   - Single staff user restriction
   - Basic admin model

### Future Improvements

- Redis integration for chat/session management
- Agent service authentication
- Enhanced admin model system

## Example Converation
![example, conversation](https://github.com/user-attachments/assets/32a72a89-4d78-4ec9-8693-914b38db4597)




