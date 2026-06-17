import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils import fetch_data, load_theme, page_header
from database.db_connection import get_connection

load_theme()

page_header(
    "Manage",
    "CRUD Operations",
    "Add, update, and remove food listings and claims from the SQL database."
)

FOOD_TYPES = ["Vegetarian", "Non-Vegetarian", "Vegan"]
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snacks"]
CLAIM_STATUSES = ["Pending", "Completed", "Cancelled"]


def execute_write(query, params):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()
        return True, None
    except Exception as exc:
        conn.rollback()
        return False, exc
    finally:
        cursor.close()
        conn.close()


def next_id(table, column):
    df = fetch_data(f"SELECT MAX({column}) AS max_id FROM {table}")
    max_id = df.iloc[0, 0]
    return int(max_id or 0) + 1


providers_df = fetch_data("""
SELECT Provider_ID,
       Name,
       Type,
       City
FROM providers
ORDER BY Provider_ID
""")

receivers_df = fetch_data("""
SELECT Receiver_ID,
       Name,
       Type,
       City
FROM receivers
ORDER BY Receiver_ID
""")

food_df = fetch_data("""
SELECT Food_ID,
       Food_Name,
       Quantity,
       Expiry_Date,
       Provider_ID,
       Provider_Type,
       Location,
       Food_Type,
       Meal_Type
FROM food_listings
ORDER BY Food_ID
""")

claims_df = fetch_data("""
SELECT Claim_ID,
       Food_ID,
       Receiver_ID,
       Status,
       Timestamp
FROM claims
ORDER BY Claim_ID
""")

tab_add_food, tab_update_food, tab_delete_food, tab_add_claim, tab_update_claim, tab_delete_claim = st.tabs(
    [
        "Add Food",
        "Update Food",
        "Delete Food",
        "Add Claim",
        "Update Claim",
        "Delete Claim"
    ]
)

provider_options = {
    f"{row.Provider_ID} - {row.Name} ({row.Type}, {row.City})": row
    for row in providers_df.itertuples(index=False)
}

food_options = {
    f"{row.Food_ID} - {row.Food_Name} ({row.Location})": row
    for row in food_df.itertuples(index=False)
}

receiver_options = {
    f"{row.Receiver_ID} - {row.Name} ({row.Type}, {row.City})": row
    for row in receivers_df.itertuples(index=False)
}

claim_options = {
    f"{row.Claim_ID} - Food {row.Food_ID} / Receiver {row.Receiver_ID} ({row.Status})": row
    for row in claims_df.itertuples(index=False)
}

with tab_add_food:
    if providers_df.empty:
        st.error("No providers found. Add providers before creating food listings.")
        st.stop()

    food_name = st.text_input("Food Name", key="add_food_name")
    quantity = st.number_input("Quantity", min_value=1, key="add_quantity")
    expiry_date = st.date_input("Expiry Date", key="add_expiry")
    selected_provider = st.selectbox("Provider", list(provider_options.keys()), key="add_provider")
    provider_row = provider_options[selected_provider]

    form_col1, form_col2 = st.columns(2)

    with form_col1:
        food_type = st.selectbox("Food Type", FOOD_TYPES, key="add_food_type")

    with form_col2:
        meal_type = st.selectbox("Meal Type", MEAL_TYPES, key="add_meal_type")

    if st.button("Add Food Listing", key="add_food_button"):
        if not food_name.strip():
            st.error("Food Name is required.")
        else:
            success, error = execute_write(
                """
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
                """,
                (
                    next_id("food_listings", "Food_ID"),
                    food_name.strip(),
                    quantity,
                    expiry_date,
                    provider_row.Provider_ID,
                    provider_row.Type,
                    provider_row.City,
                    food_type,
                    meal_type
                )
            )

            if success:
                st.success("Food listing added successfully.")
            else:
                st.error(f"Error adding food listing: {error}")

with tab_update_food:
    if food_df.empty:
        st.info("No food listings available to update.")
    else:
        selected_food = st.selectbox("Food Listing", list(food_options.keys()), key="update_food")
        food_row = food_options[selected_food]
        provider_key = next(
            key for key, row in provider_options.items()
            if row.Provider_ID == food_row.Provider_ID
        )

        updated_name = st.text_input("Food Name", value=food_row.Food_Name, key="update_food_name")
        updated_quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=int(food_row.Quantity),
            key="update_quantity"
        )
        updated_expiry = st.date_input(
            "Expiry Date",
            value=food_row.Expiry_Date,
            key="update_expiry"
        )
        updated_provider_key = st.selectbox(
            "Provider",
            list(provider_options.keys()),
            index=list(provider_options.keys()).index(provider_key),
            key="update_provider"
        )
        updated_provider = provider_options[updated_provider_key]

        form_col1, form_col2 = st.columns(2)

        with form_col1:
            updated_food_type = st.selectbox(
                "Food Type",
                FOOD_TYPES,
                index=FOOD_TYPES.index(food_row.Food_Type) if food_row.Food_Type in FOOD_TYPES else 0,
                key="update_food_type"
            )

        with form_col2:
            updated_meal_type = st.selectbox(
                "Meal Type",
                MEAL_TYPES,
                index=MEAL_TYPES.index(food_row.Meal_Type) if food_row.Meal_Type in MEAL_TYPES else 0,
                key="update_meal_type"
            )

        if st.button("Update Food Listing", key="update_food_button"):
            if not updated_name.strip():
                st.error("Food Name is required.")
            else:
                success, error = execute_write(
                    """
                    UPDATE food_listings
                    SET Food_Name = %s,
                        Quantity = %s,
                        Expiry_Date = %s,
                        Provider_ID = %s,
                        Provider_Type = %s,
                        Location = %s,
                        Food_Type = %s,
                        Meal_Type = %s
                    WHERE Food_ID = %s
                    """,
                    (
                        updated_name.strip(),
                        updated_quantity,
                        updated_expiry,
                        updated_provider.Provider_ID,
                        updated_provider.Type,
                        updated_provider.City,
                        updated_food_type,
                        updated_meal_type,
                        food_row.Food_ID
                    )
                )

                if success:
                    st.success("Food listing updated successfully.")
                else:
                    st.error(f"Error updating food listing: {error}")

with tab_delete_food:
    if food_df.empty:
        st.info("No food listings available to delete.")
    else:
        selected_food_delete = st.selectbox(
            "Food Listing",
            list(food_options.keys()),
            key="delete_food"
        )
        food_delete_row = food_options[selected_food_delete]
        st.warning("Deleting a food listing also deletes related claims first.")

        if st.button("Delete Food Listing", key="delete_food_button"):
            conn = get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "DELETE FROM claims WHERE Food_ID = %s",
                    (food_delete_row.Food_ID,)
                )
                cursor.execute(
                    "DELETE FROM food_listings WHERE Food_ID = %s",
                    (food_delete_row.Food_ID,)
                )
                conn.commit()
                st.success("Food listing and related claims deleted successfully.")
            except Exception as exc:
                conn.rollback()
                st.error(f"Error deleting food listing: {exc}")
            finally:
                cursor.close()
                conn.close()

with tab_add_claim:
    if food_df.empty or receivers_df.empty:
        st.error("Food listings and receivers are required before creating claims.")
    else:
        selected_claim_food = st.selectbox("Food Listing", list(food_options.keys()), key="claim_food")
        selected_receiver = st.selectbox("Receiver", list(receiver_options.keys()), key="claim_receiver")
        claim_status = st.selectbox("Claim Status", CLAIM_STATUSES, key="claim_status")

        if st.button("Add Claim", key="add_claim_button"):
            success, error = execute_write(
                """
                INSERT INTO claims
                (
                    Claim_ID,
                    Food_ID,
                    Receiver_ID,
                    Status,
                    Timestamp
                )
                VALUES (%s,%s,%s,%s,NOW())
                """,
                (
                    next_id("claims", "Claim_ID"),
                    food_options[selected_claim_food].Food_ID,
                    receiver_options[selected_receiver].Receiver_ID,
                    claim_status
                )
            )

            if success:
                st.success("Claim added successfully.")
            else:
                st.error(f"Error adding claim: {error}")

with tab_update_claim:
    if claims_df.empty:
        st.info("No claims available to update.")
    else:
        selected_claim = st.selectbox("Claim", list(claim_options.keys()), key="update_claim")
        claim_row = claim_options[selected_claim]

        current_status_index = (
            CLAIM_STATUSES.index(claim_row.Status)
            if claim_row.Status in CLAIM_STATUSES
            else 0
        )
        updated_status = st.selectbox(
            "Claim Status",
            CLAIM_STATUSES,
            index=current_status_index,
            key="update_claim_status"
        )

        if st.button("Update Claim Status", key="update_claim_button"):
            success, error = execute_write(
                """
                UPDATE claims
                SET Status = %s,
                    Timestamp = NOW()
                WHERE Claim_ID = %s
                """,
                (
                    updated_status,
                    claim_row.Claim_ID
                )
            )

            if success:
                st.success("Claim updated successfully.")
            else:
                st.error(f"Error updating claim: {error}")

with tab_delete_claim:
    if claims_df.empty:
        st.info("No claims available to delete.")
    else:
        selected_claim_delete = st.selectbox(
            "Claim",
            list(claim_options.keys()),
            key="delete_claim"
        )
        claim_delete_row = claim_options[selected_claim_delete]

        if st.button("Delete Claim", key="delete_claim_button"):
            success, error = execute_write(
                "DELETE FROM claims WHERE Claim_ID = %s",
                (claim_delete_row.Claim_ID,)
            )

            if success:
                st.success("Claim deleted successfully.")
            else:
                st.error(f"Error deleting claim: {error}")
