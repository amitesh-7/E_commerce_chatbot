# E-Commerce Expert Assistant Chatbot

## Summary
This project is an AI-powered e-commerce chatbot built to answer questions about product details and customer orders, as part of the Engineering Chatbot Challenge. [cite: 1, 2]

## Architecture
The system is built using a microservices architecture with three main services: [cite: 31]
* **chat-service**: The main entry point that routes user input and communicates with the LLM. [cite: 33]
* **product-search-service**: A RAG-based service for retrieving product details. [cite: 34]
* **order-lookup-service**: A mock API for fetching customer order history. [cite: 35]

## How to Run Locally
1.  Ensure you have Docker Desktop installed and running.
2.  Create a `.env` file in the root directory and add your `GEMINI_API_KEY`.
3.  Run the indexing script: `python product-search-service/create_index.py`
4.  Start the services: `docker-compose up --build`

## Testing Instructions
To test the chatbot, send a POST request to the main chat endpoint. [cite: 60]

### Product Question
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"What are some good bass guitars?\", \"session_id\": \"user123\"}"

### Order Question
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"What is the status of my orders for customer 37077?\", \"session_id\": \"user456\"}"