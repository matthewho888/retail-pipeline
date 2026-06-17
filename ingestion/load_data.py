import pandas as pd
from sqlalchemy import create_engine
import os

# Connection to PostgreSQL
engine = create_engine(
    "postgresql://retail_user:retail_pass@localhost:5432/retail_db"
)

# Path to data folder
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

# Map CSV files to table names
datasets = {
    "olist_customers_dataset.csv": "raw_customers",
    "olist_orders_dataset.csv": "raw_orders",
    "olist_order_items_dataset.csv": "raw_order_items",
    "olist_order_payments_dataset.csv": "raw_order_payments",
    "olist_order_reviews_dataset.csv": "raw_order_reviews",
    "olist_products_dataset.csv": "raw_products",
    "olist_sellers_dataset.csv": "raw_sellers",
    "olist_geolocation_dataset.csv": "raw_geolocation",
    "product_category_name_translation.csv": "raw_category_translation",
}

def load_all():
    with engine.connect() as conn:
        for filename, table_name in datasets.items():
            filepath = os.path.join(DATA_PATH, filename)
            print(f"Loading {filename} → {table_name}...")
            df = pd.read_csv(filepath)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.commit()
            print(f"  ✔ {len(df)} rows loaded")

if __name__ == "__main__":
    load_all()