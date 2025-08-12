import os
import httpx
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "null", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    genai.configure(api_key=os.getenv("API_KEY"))
    llm = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Warning: Could not configure Gemini. Error: {e}")
    llm = None

ORDER_API_BASE_URL = "http://order-lookup-service:8000/data"
PRODUCT_API_URL = "http://host.docker.internal:8002/search"

class ChatQuery(BaseModel):
    query: str
    session_id: str

def classify_intent_and_extract_entities(query: str):
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
    if not llm:
        raise HTTPException(status_code=503, detail="LLM is not available. Check API Key.")

    intent, entities = classify_intent_and_extract_entities(chat_query.query)
    context = ""
    
    if intent == "ORDER_INQUIRY_NO_ID":
        return {"response": "I can help with order information. Could you please provide your Customer ID?"}

    timeout = httpx.Timeout(30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(3):
            try:
                if intent == "ORDER_BY_CUSTOMER_ID":
                    customer_id = entities.get("customer_id")
                    api_url = f"{ORDER_API_BASE_URL}/customer/{customer_id}"
                    response = await client.get(api_url)
                    response.raise_for_status() # Raise an exception for bad status codes
                    response_data = response.json()
                    if isinstance(response_data, dict) and "error" in response_data:
                        context = f"Context: {response_data['error']}"
                    else:
                        context = "Context from order history:\n" + "\n".join(
                            [f"- Order on {o.get('Order_Date', 'N/A')} for '{o.get('Product_Category', 'N/A')}' with priority '{o.get('Order_Priority', 'N/A')}'" for o in response_data[:5]]
                        )

                elif intent == "PRODUCT_SEARCH":
                    response = await client.post(PRODUCT_API_URL, json={"query": chat_query.query})
                    response.raise_for_status()
                    products = response.json()
                    context = "Context from product search:\n" + "\n".join([f"- Title: {p['title']}, Price: ${p.get('price', 'N/A')}, Rating: {p.get('average_rating', 'N/A')}" for p in products])
                
                break

            except httpx.RequestError as e:
                context = f"Context: Could not connect to the service. Attempt {attempt + 1} of 3."
                time.sleep(2)
    
    prompt = f"""You are a helpful and friendly e-commerce assistant. 
    Your primary goal is to answer the user's question based ONLY on the context provided below.

    **Context:**
    {context}

    **User Question:**
    {chat_query.query}

    Based strictly on the context above, answer the user's question. If the user's question contains multiple parts, only answer the part that is relevant to the provided context. Ignore any parts of the question that are not related to the context.
    """
    
    llm_response = llm.generate_content(prompt)
    return {"response": llm_response.text}