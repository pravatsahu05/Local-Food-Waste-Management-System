# Local Food Waste Management System

A Streamlit and MySQL based application for managing surplus food donations, connecting providers with receivers, tracking claims, and analyzing food wastage trends.

## Project Overview

Food wastage is a major issue while many people still face food insecurity. This project provides a local food redistribution platform where restaurants, grocery stores, supermarkets, and catering services can list surplus food, and NGOs or individuals can identify and claim available food.

The app includes a modern dark themed Streamlit interface, SQL-powered analysis, CRUD operations, location-based exploration, and visual dashboards.

## Features

- Modern Streamlit dark theme UI
- Provider and receiver directory
- Food listings with filters by city, provider, food type, and meal type
- Claims tracking with status filtering
- Full CRUD operations for food listings
- Claim creation, status update, and deletion
- SQL analysis page with 20 business queries
- Dashboard with KPI cards and high-priority expiring food
- Analytics page with provider, city, claim, meal, and expiry insights
- Location Explorer for city-wise availability and contacts
- CSV result downloads for SQL analysis

## Tech Stack

- Python
- Streamlit
- MySQL
- Pandas
- Plotly
- SQL

## Project Structure

```text
Local_Food_Waste_Management_System/
├── app/
│   ├── Home.py
│   ├── utils.py
│   └── pages/
│       ├── Claims.py
│       ├── CRUD.py
│       ├── Dashboard.py
│       ├── Food_Listings.py
│       ├── Location_Explorer.py
│       ├── Providers.py
│       ├── SQL_Analysis.py
│       └── Visualizations.py
├── data/
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   ├── claims_data.csv
│   └── *_cleaned.csv
├── database/
│   ├── create_tables.sql
│   ├── clean_dataset.py
│   ├── data_cleaning.py
│   ├── db_connection.py
│   ├── insert_data.py
│   └── verify_data.py
├── sql_queries/
│   ├── queries.py
│   └── test_queries.py
├── visuals/
├── requirements.txt
└── README.md
```

## Dataset

The project uses four datasets:

- `providers_data.csv`: food provider information
- `receivers_data.csv`: food receiver information
- `food_listings_data.csv`: available food listings
- `claims_data.csv`: receiver claims and claim status

## Database Tables

The MySQL database contains:

- `providers`
- `receivers`
- `food_listings`
- `claims`

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Local_Food_Waste_Management_System.git
cd Local_Food_Waste_Management_System
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create the database and tables using:

```bash
mysql -u root -p < database/create_tables.sql
```

Set your database credentials as environment variables.

On Windows PowerShell:

```powershell
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_NAME="food_waste_management"
```

On macOS/Linux:

```bash
export DB_HOST="127.0.0.1"
export DB_PORT="3306"
export DB_USER="root"
export DB_PASSWORD="your_mysql_password"
export DB_NAME="food_waste_management"
```

### 5. Clean and Insert Data

```bash
python database/clean_dataset.py
python database/insert_data.py
python database/verify_data.py
```

### 6. Run SQL Query Test

```bash
python sql_queries/test_queries.py
```

### 7. Run the Streamlit App

```bash
streamlit run app/Home.py
```

Open the app in your browser:

```text
http://localhost:8501
```

## SQL Analysis Questions Covered

The app includes 20 SQL queries, including:

- Providers per city
- Receivers per city
- Top contributing provider type
- Provider contact information
- Top claiming receivers
- Total available food quantity
- City with most food listings
- Common food types
- Claims per food item
- Most successful provider
- Claim status percentage
- Average quantity claimed per receiver
- Most claimed meal type
- Total donated quantity per provider
- Expiring soon food listings
- Food by meal type
- Food by city
- Completed claims
- Pending claims
- Cancelled claims

## App Pages

### Home

Project introduction, live data-driven insight cards, and feature overview.

### Dashboard

Operational KPIs, provider contribution chart, claim status chart, and urgent expiring food cards.

### Food Listings

Search and filter available food by food name, city, provider, food type, and meal type.

### Providers

Provider and receiver contact directory for coordination.

### Claims

Claim tracking with status summaries and filtered claim records.

### CRUD

Add, update, and delete food listings. Add, update, and delete claims.

### SQL Analysis

Run 20 predefined SQL queries and download the result as CSV.

### Visualizations

EDA charts for provider contribution, city supply, claim demand, meal demand, and expiry trends.

### Location Explorer

City-wise food availability, provider contacts, receiver contacts, and location insights.

## Project Evaluation Coverage

- Data cleaning and preparation: implemented
- SQL database creation: implemented
- SQL queries and analysis: implemented with 20 queries
- Streamlit interface: implemented
- Filtering options: implemented
- Provider and receiver contact details: implemented
- CRUD operations: implemented
- Visualizations and EDA: implemented
- Location-based exploration: implemented using available city/location data

## Streamlit Cloud Deployment

Streamlit Cloud cannot connect to a MySQL database running on your laptop with `127.0.0.1`. For deployment, create a cloud MySQL database, import the project tables and data, then add the cloud database credentials in Streamlit secrets.

Use these deployment settings:

```text
Repository: pravatsahu05/Local-Food-Waste-Management-System
Branch: main
Main file path: app/Home.py
```

Add these secrets in Streamlit Cloud:

```toml
DB_HOST = "your_cloud_mysql_host"
DB_PORT = "3306"
DB_USER = "your_cloud_mysql_user"
DB_PASSWORD = "your_cloud_mysql_password"
DB_NAME = "food_waste_management"
```

## Notes

- The dataset contains city/location fields but does not contain latitude and longitude, so the location feature is implemented as a city-based explorer.
- Do not commit `.env`, `.streamlit/secrets.toml`, or local credentials.
- Keep `venv/` out of GitHub. It is excluded in `.gitignore`.

## Author

Created as a capstone-style project for local food waste reduction and food redistribution analysis.
