# Sample Questions & Answers

This document contains sample interactions with the E-Commerce Chatbot, demonstrating its ability to answer questions from both the product and order datasets.

## Product Dataset Queries

### 1. Specific Product Inquiry

**Command:**
```bash
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"Tell me about the BOYA BYM1 Microphone.\", \"session_id\": \"test1\"}"
Chatbot Response:

JSON

{
    "response": "The Boya BYM1 is a shotgun video microphone with a 3.5mm connector.  It's described as an omnidirectional condenser microphone, and is designed to clip on for video recording. It's compatible with iPhones, Android smartphones, Macs, tablets, DSLRs, and camcorders.  The price is $14.95 and it has a 4.0-star rating.\n"
}
2. Top-Rated Product Inquiry
Command:

Bash

curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"What are the top-rated guitar products?\", \"session_id\": \"test2\"}"
Chatbot Response:

JSON

{
    "response": "Based on the product search results, the top-rated guitar products are:\n\n1. **Perri’s Leathers Guitar Picks - AC/DC Official Licensed Banjo Guitar Pick Set:** 4.7 stars\n2. **Guitar Picks Surmoler 6 Pack Universal Plastic Guitar Picks:** 4.7 stars\n3. **JIM DUNLOP DHCN1048 Heavy Core Guitar Strings:** 4.7 stars\n4. **Perri's Leathers Ltd. - Guitar Picks - Celluloid - Iron Maiden - Official Licensed Product:** 4.8 stars\n\nPlease note that the LAGRIMA Acoustic Guitar is excluded because its price is unavailable.\n"
}
3. Price-Based Inquiry
Command:

Bash

curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"I need a cheap guitar stand.\", \"session_id\": \"test3\"}"
Chatbot Response:

JSON

{
    "response": "Based on the products I found, the Smiger Flexible adjustment Guitar Stand is the cheapest option at $20.99.  Keep in mind that two other guitar stands have prices listed as \"None,\" so there may be cheaper options available that aren't currently showing their price.\n"
}
Order Dataset Queries
1. Most Recent Order Inquiry
Command:

Bash

curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"What are the details of my most recent order? My Customer ID is 37077.\", \"session_id\": \"test6\"}"
Chatbot Response:

JSON

{
    "response": "I see you're looking for details on your most recent order, Customer ID 37077.  Based on my order history, your most recent order was placed on January 2nd, 2018, for Auto & Accessories.  The priority level for that order was Medium.  I don't have further details like the specific items ordered or the total cost available at this time.\n"
}
2. General Order History Inquiry
Command:

Bash

curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"query\": \"Show me the order history for customer 35081.\", \"session_id\": \"test8\"}"
Chatbot Response:

JSON

{
    "response": "I can see one order in your history for customer 35081.  On December 30th, 2018, an order was placed for Auto & Accessories with a priority marked as Critical.\n"
}