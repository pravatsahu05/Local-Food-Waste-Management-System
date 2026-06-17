import pandas as pd

# Load datasets
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

print("\n========== PROVIDERS ==========")
print(providers.head())
print(providers.info())
print(providers.isnull().sum())
print("Duplicates:", providers.duplicated().sum())

print("\n========== RECEIVERS ==========")
print(receivers.head())
print(receivers.info())
print(receivers.isnull().sum())
print("Duplicates:", receivers.duplicated().sum())

print("\n========== FOOD LISTINGS ==========")
print(food.head())
print(food.info())
print(food.isnull().sum())
print("Duplicates:", food.duplicated().sum())

print("\n========== CLAIMS ==========")
print(claims.head())
print(claims.info())
print(claims.isnull().sum())
print("Duplicates:", claims.duplicated().sum())