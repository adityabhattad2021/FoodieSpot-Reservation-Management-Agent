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

# Agent State Transition flow
![FoodSpot Agent Flow](https://github.com/user-attachments/assets/087b86e1-ca02-4e95-8105-612d69717dcb)

## Project Structure
```
.
├── agents/                 # AI Agent Service
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── foodiespot_agent.py  # Main agent logic
│   │   │   ├── restaurants.json     # Sample restaurant data, already loaded in Pinecone
│   │   │   ├── tools/                # Work in progress (not used in current state)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── reservation_management.py
│   │   │   ├── utils/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api_client.py
│   │   │   │   ├── llm_client.py
│   │   │   │   └── prompts.py
│   │   │   └── vector_store.py  # Functions to interact with Pinecone vector database
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── session_manager.py
│   └── requirements.txt  # Agent dependencies
├── backend/               # Backend Service
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── app/
│   │   ├── auth.py        # Authentication logic
│   │   ├── crud.py        # Database operations
│   │   ├── database.py    # Database configuration
│   │   ├── init_db.py     # Database initialization
│   │   ├── main.py        # Backend entry point
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Data validation schemas
│   │   └── seed.py        # Initial data seeding
│   └── requirements.txt   # Backend dependencies
├── frontend/              # React Frontend
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Application pages
│   │   └── context/       # Auth Context for admin dashboard
├── docker-compose.yml      # Production Docker Compose
└── docker-compose.dev.yml  # Development Docker Compose with hot-reload

```

## Setup Instructions

### Prerequisites

Before you begin, ensure you have:
- Docker and Docker Compose installed
- Groq API key
- Pinecone API key

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

   # Add your Groq API key and Pinecone API key to .env
   GROQ_API_KEY=your_api_key_here
   PINECONE_API_KEY=your_api_key_here

   ```

3. **Launch Services**
   ```bash
   # Start all services
   docker-compose up --build
   ```
   ```
   # For development mode (hot-reload)
   docker-compose -f docker-compose.dev.yml up --build
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

> Reference: [prompts.py](agents/app/core/utils/prompts.py) 

### Key Design Elements (In order)

1. **Role Definition & Scope Enforcement**
   ```python
   "You are FoodieBot, a friendly restaurant recommendation assistant. Your goal is to help users find restaurants based ONLY on the information provided in context."
   ```


2. **Core Rules & Response Structure**
   ```python
   "## CORE RULES:
   1. ONLY use restaurants from the query context—never make up details.
   2. Use short, simple sentences and avoid fancy words.
   3. Keep responses brief: 1-2 sentences per recommendation.
   4. Remember the restaurant you're talking about and stick to it unless the user asks for alternatives.
   5. Strictly use markdown formatting for all responses."
   ```

3. **Query-Specific Response Templates**
   ```python
   "## RESPONSE ORDER:
   1. Name and Location: "I recommend [Name] in [Location]."
   2. Price and Cuisine: "It's a [price range] [cuisine] spot."
   3. Key Info: "They have [feature] and [dietary option]."
   4. Specialties: "Try their [dish 1] or [dish 2].""
   ```

4. **Extensive Few-Shot Examples**
   ```python
   "## Example 1: Basic Recommendation
   User: "I'm looking for Indian food in Indiranagar"
   FoodieBot: I recommend **Punjabi Dhaba** in Indiranagar. It's a *North Indian* restaurant with outdoor seating."
   ```
   - Demonstrates ideal conversation flows


5. **Error Handling & Recovery Patterns**
   ```python
   "### Out-of-Context Queries:
   - Say: "I don't see that in the results." Then: "Here's [available option] instead.""
   ```

#### Limitations
 - Even with current design, the agent sometimes fails to understand the user intent and provides incorrect response.
 - This can be improved by using a better model.

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

- Implement voice-based interaction
- Implement a feedback system for user ratings
- Use an LLM model with better language understanding

## Example Converation

[![FoodieSpot Demo Youtube Thumbnail](https://github.com/user-attachments/assets/cd6f1eda-3879-4ba9-bc39-f08221eb3767)](https://youtu.be/OJEZVylg6FQ)
