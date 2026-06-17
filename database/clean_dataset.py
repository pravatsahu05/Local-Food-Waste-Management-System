import pandas as pd

providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

# Remove duplicates
providers.drop_duplicates(inplace=True)
receivers.drop_duplicates(inplace=True)
food.drop_duplicates(inplace=True)
claims.drop_duplicates(inplace=True)

# Remove spaces from column names
providers.columns = providers.columns.str.strip()
receivers.columns = receivers.columns.str.strip()
food.columns = food.columns.str.strip()
claims.columns = claims.columns.str.strip()

# Convert date columns
food["Expiry_Date"] = pd.to_datetime(
    food["Expiry_Date"],
    errors="coerce"
)

claims["Timestamp"] = pd.to_datetime(
    claims["Timestamp"],
    errors="coerce"
)

# Save cleaned files
providers.to_csv(
    "data/providers_cleaned.csv",
    index=False
)

receivers.to_csv(
    "data/receivers_cleaned.csv",
    index=False
)

food.to_csv(
    "data/food_listings_cleaned.csv",
    index=False
)

claims.to_csv(
    "data/claims_cleaned.csv",
    index=False
)

print("Cleaning Completed Successfully")