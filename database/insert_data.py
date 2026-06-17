import pandas as pd
from db_connection import get_connection

# Database Connection
conn = get_connection()
cursor = conn.cursor()

# =========================
# PROVIDERS
# =========================

providers = pd.read_csv("data/providers_cleaned.csv")

for _, row in providers.iterrows():
    cursor.execute("""
        INSERT INTO providers
        (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        int(row["Provider_ID"]),
        row["Name"],
        row["Type"],
        row["Address"],
        row["City"],
        str(row["Contact"])
    ))

print("Providers Imported")

# =========================
# RECEIVERS
# =========================

receivers = pd.read_csv("data/receivers_cleaned.csv")

for _, row in receivers.iterrows():
    cursor.execute("""
        INSERT INTO receivers
        (Receiver_ID, Name, Type, City, Contact)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        int(row["Receiver_ID"]),
        row["Name"],
        row["Type"],
        row["City"],
        str(row["Contact"])
    ))

print("Receivers Imported")

# =========================
# FOOD LISTINGS
# =========================

food = pd.read_csv("data/food_listings_cleaned.csv")

food["Expiry_Date"] = pd.to_datetime(
    food["Expiry_Date"]
).dt.date

for _, row in food.iterrows():

    cursor.execute("""
        INSERT INTO food_listings
        (
            Food_ID,
            Food_Name,
            Quantity,
            Expiry_Date,
            Provider_ID,
            Provider_Type,
            Location,
            Food_Type,
            Meal_Type
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        int(row["Food_ID"]),
        row["Food_Name"],
        int(row["Quantity"]),
        row["Expiry_Date"],
        int(row["Provider_ID"]),
        row["Provider_Type"],
        row["Location"],
        row["Food_Type"],
        row["Meal_Type"]
    ))

print("Food Listings Imported")

# =========================
# CLAIMS
# =========================

claims = pd.read_csv("data/claims_cleaned.csv")

claims["Timestamp"] = pd.to_datetime(
    claims["Timestamp"]
)

for _, row in claims.iterrows():

    cursor.execute("""
        INSERT INTO claims
        (
            Claim_ID,
            Food_ID,
            Receiver_ID,
            Status,
            Timestamp
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        int(row["Claim_ID"]),
        int(row["Food_ID"]),
        int(row["Receiver_ID"]),
        row["Status"],
        row["Timestamp"]
    ))

print("Claims Imported")

# Commit Changes
conn.commit()

print("\nAll Data Imported Successfully")

cursor.close()
conn.close()