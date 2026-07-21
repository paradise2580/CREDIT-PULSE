"""One-time load: push train.csv into Neon PostgreSQL as churn_data."""

import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, ".env"))

CSV_PATH = os.path.join(ROOT, "Machine learning Models", "Neural_Networks", "train.csv")


def main():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("Set DATABASE_URL in .env first")

    if not url.startswith("postgresql://"):
        raise SystemExit("DATABASE_URL must start with postgresql://")

    engine = create_engine(url)
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.lower() for c in df.columns]

    print(f"Loading {len(df)} rows into churn_data...")
    df.to_sql("churn_data", engine, if_exists="replace", index=False, chunksize=5000, method="multi")

    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE churn_data ADD PRIMARY KEY (id)"))

    print("Done. Table churn_data is ready.")


if __name__ == "__main__":
    main()
