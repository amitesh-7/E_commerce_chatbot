import os
import httpx
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

try:
    genai.configure(api_key=os.getenv("API_KEY"))
    llm = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Warning: Could not configure Gemini. LLM will not be available. Error: {e}")
    llm = None

# This URL points to the other container by its service name.
ORDER_API_BASE_URL = "http://order-lookup-service:8000/data"

# This URL uses a special Docker hostname to connect back to the host machine,
# bypassing potential container-to-container DNS issues.
PRODUCT_API_URL = "http://host.docker.internal:8002/search"


class ChatQuery(BaseModel):
    query: str
    session_id: str

def classify_intent_and_extract_entities(query: str):
    """
    Parses the user query to determine intent and extract relevant details.
    """
    query_lower = query.lower()
    order_keywords = ["order", "purchase", "shipping", "status", "my last"]
    customer_id_match = re.search(r'\b\d{5,}\b', query)
    customer_id = customer_id_match.group(0) if customer_id_match else None

    if any(keyword in query_lower for keyword in order_keywords) or customer_id:
        if customer_id:
            return "ORDER_BY_CUSTOMER_ID", {"customer_id": customer_id}
        else:
            return "ORDER_INQUIRY_NO_ID", {}
    
    return "PRODUCT_SEARCH", {}

@app.post("/chat")
async def chat(chat_query: ChatQuery):
    """
    Main chat endpoint that routes requests based on user intent.
    """
    if not llm:
        raise HTTPException(status_code=503, detail="LLM is not available. Check API Key.")

    intent, entities = classify_intent_and_extract_entities(chat_query.query)
    context = ""
    
    if intent == "ORDER_INQUIRY_NO_ID":
        return {"response": "I can help with order information. Could you please provide your Customer ID?"}

    async with httpx.AsyncClient(timeout=20.0) as client:
        if intent == "ORDER_BY_CUSTOMER_ID":
            customer_id = entities.get("customer_id")
            api_url = f"{ORDER_API_BASE_URL}/customer/{customer_id}"
            try:
                response = await client.get(api_url)
                response_data = response.json()
                if isinstance(response_data, dict) and "error" in response_data:
                    context = f"Context: {response_data['error']}"
                else:
                    context = "Context from order history:\n" + "\n".join(
                        [f"- Order on {o.get('Order_Date', 'N/A')} for '{o.get('Product_Category', 'N/A')}' with priority '{o.get('Order_Priority', 'N/A')}'" for o in response_data[:5]]
                    )
            except httpx.RequestError as e:
                context = f"Context: Could not connect to the order service: {e}"

        elif intent == "PRODUCT_SEARCH":
            try:
                response = await client.post(PRODUCT_API_URL, json={"query": chat_query.query})
                products = response.json()
                context = "Context from product search:\n" + "\n".join([f"- Title: {p['title']}, Price: ${p.get('price', 'N/A')}, Rating: {p.get('average_rating', 'N/A')}" for p in products])
            except httpx.RequestError as e:
                context = f"Context: Could not connect to the product service: {e}"

    prompt = f"""You are a helpful and friendly e-commerce assistant.
    Use the provided context to answer the user's question.
    If the context says no data was found, inform the user politely.
    If there is no context, answer the question based on general knowledge.

    {context}

    User Question: {chat_query.query}

    Answer:"""
    
    llm_response = llm.generate_content(prompt)
    return {"response": llm_response.text}