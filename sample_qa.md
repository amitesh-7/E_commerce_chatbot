# Sample Questions & Answers

This document contains sample interactions with the E-Commerce Chatbot, demonstrating its ability to answer questions from both the product and order datasets.

## Product Dataset Queries

### 1. Specific Product Inquiry

**User Question:**
`Tell me about the BOYA BYM1 Microphone.`

**Chatbot Response:**
```json
{
    "response": "The Boya BYM1 is a shotgun video microphone. It's a 3.5mm lapel mic that clips on, is omnidirectional and condenser, and is designed for video recording. It works with iPhones, Android smartphones, Macs, tablets, DSLRs, and camcorders. It costs $14.95 and has a 4.0 rating."
}
2. Top-Rated Product Inquiry
User Question:
What are the top-rated guitar products?

Chatbot Response:

JSON

{
    "response": "Based on the provided product listings, the top-rated guitar products are: * Perri’s Leathers Guitar Picks - AC/DC Official Licensed Banjo Guitar Pick Set (4.7 rating) * Guitar Picks Surmoler 6 Pack (4.7 rating) * JIM DUNLOP DHCN1048 Heavy Core Guitar Strings (4.7 rating) * Perri's Leathers Ltd. - Guitar Picks - Celluloid - Iron Maiden (4.8 rating)"
}
3. Price-Based Inquiry
User Question:
I need a cheap guitar stand.

Chatbot Response:

JSON

{
    "response": "Based on the provided options, the cheapest guitar stand is the Smiger Flexible adjustment Guitar Stand for $20.99."
}
Order Dataset Queries
1. General Order History Inquiry
User Question:
Show me the order history for customer 35081.

Chatbot Response:

JSON

{
    "response": "On 2018-12-30, customer 35081 placed an order for Auto & Accessories with priority set to Critical."
}
2. Confusing Multi-Part Inquiry
User Question:
What are some good guitars? or check my order for customer 37077

Chatbot Response:

JSON

{
    "response": "Based on your order history, you placed an order for Auto & Accessories on 2018-01-02 with medium priority."
}