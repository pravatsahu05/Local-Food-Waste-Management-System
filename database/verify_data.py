from db_connection import get_connection
import pandas as pd

conn = get_connection()

tables = [
    "providers",
    "receivers",
    "food_listings",
    "claims"
]

for table in tables:

    query = f"SELECT COUNT(*) AS Total FROM {table}"

    df = pd.read_sql(query, conn)

    print(f"\n{table}")
    print(df)

conn.close()