from fastapi import FastAPI
import pandas as pd

DATASET_PATH = "/app/data/Order_details.csv"

app = FastAPI(
    title="E-commerce Dataset API",
    description="API for querying e-commerce sales data",
)

try:
    df = pd.read_csv(DATASET_PATH)
    numeric_cols = df.select_dtypes(include=['number']).columns
    string_cols = df.select_dtypes(include=['object']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[string_cols] = df[string_cols].fillna("")
except FileNotFoundError:
    print(f"FATAL ERROR: Dataset not found at {DATASET_PATH}")
    df = pd.DataFrame()

@app.get("/data/customer/{customer_id}")
def get_customer_data(customer_id: int):
    filtered_data = df[df["Customer_Id"] == customer_id]
    if filtered_data.empty:
        return {"error": f"No data found for Customer ID {customer_id}"}
    return filtered_data.to_dict(orient="records")

@app.get("/data/order-priority/{priority}")
def get_orders_by_priority(priority: str):
    """Retrieve all orders with the given priority."""
    filtered_data = df[df["Order_Priority"].str.contains(priority, case=False, na=False)]
    if filtered_data.empty:
        return {"error": f"No data found for Order Priority '{priority}'"}
    return filtered_data.to_dict(orient="records")