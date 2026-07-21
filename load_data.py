import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
db_url = os.environ.get("database_url")

# Read the CSV from its actual location
df = pd.read_csv("Machine learning Models/Neural_Networks/train.csv")

# Rename columns to lowercase to match what app.py expects
df.columns = [col.lower() for col in df.columns]

# Connect to Neon database
engine = create_engine(db_url)

# Push the dataframe into a table called churn_data
df.to_sql("churn_data", engine, if_exists="replace", index=False)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE churn_data ADD PRIMARY KEY (id);"))
    conn.commit()

print("Done! churn_data table created with", len(df), "rows.")