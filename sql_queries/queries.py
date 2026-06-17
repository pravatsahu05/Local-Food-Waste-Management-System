import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database.db_connection import get_connection
import pandas as pd


def run_query(query):
    conn = get_connection()

    df = pd.read_sql(query, conn)

    conn.close()

    return df

QUERIES = {

    "Q1_Providers_Per_City": """
        SELECT City,
               COUNT(*) AS Total_Providers
        FROM providers
        GROUP BY City
        ORDER BY Total_Providers DESC;
    """,

    "Q2_Receivers_Per_City": """
        SELECT City,
               COUNT(*) AS Total_Receivers
        FROM receivers
        GROUP BY City
        ORDER BY Total_Receivers DESC;
    """,

    "Q3_Top_Provider_Type": """
        SELECT Provider_Type,
               SUM(Quantity) AS Total_Food
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Food DESC;
    """,

    "Q4_Provider_Contacts": """
        SELECT Name,
               City,
               Contact
        FROM providers;
    """,

    "Q5_Top_Claiming_Receivers": """
        SELECT r.Name,
               COUNT(*) AS Total_Claims
        FROM claims c
        JOIN receivers r
        ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name
        ORDER BY Total_Claims DESC;
    """,

    "Q6_Total_Food_Available": """
        SELECT SUM(Quantity) AS Total_Food
        FROM food_listings;
    """,

    "Q7_City_With_Most_Listings": """
        SELECT Location,
               COUNT(*) AS Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Listings DESC;
    """,

    "Q8_Common_Food_Types": """
        SELECT Food_Type,
               COUNT(*) AS Total
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Total DESC;
    """,

    "Q9_Claims_Per_Food": """
        SELECT f.Food_Name,
               COUNT(*) AS Claims
        FROM claims c
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        GROUP BY f.Food_Name
        ORDER BY Claims DESC;
    """,

    "Q10_Most_Successful_Provider": """
        SELECT p.Name,
               COUNT(*) AS Successful_Claims
        FROM claims c
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        JOIN providers p
        ON p.Provider_ID=f.Provider_ID
        WHERE c.Status='Completed'
        GROUP BY p.Name
        ORDER BY Successful_Claims DESC;
    """,

    "Q11_Claim_Status_Percentage": """
        SELECT Status,
               ROUND(
                   COUNT(*)*100/
                   (SELECT COUNT(*) FROM claims),
                   2
               ) AS Percentage
        FROM claims
        GROUP BY Status;
    """,

    "Q12_Avg_Quantity_Claimed": """
        SELECT r.Name,
               AVG(f.Quantity) AS Avg_Quantity
        FROM claims c
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        JOIN receivers r
        ON c.Receiver_ID=r.Receiver_ID
        GROUP BY r.Name
        ORDER BY Avg_Quantity DESC;
    """,

    "Q13_Most_Claimed_Meal_Type": """
        SELECT Meal_Type,
               COUNT(*) AS Claims
        FROM claims c
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        GROUP BY Meal_Type
        ORDER BY Claims DESC;
    """,

    "Q14_Total_Donated_Per_Provider": """
        SELECT p.Name,
               SUM(f.Quantity) AS Total_Donated
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        GROUP BY p.Name
        ORDER BY Total_Donated DESC;
    """,

    "Q15_Expiring_Soon": """
        SELECT *
        FROM food_listings
        WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY;
    """,

    "Q16_Food_By_Meal_Type": """
        SELECT Meal_Type,
            SUM(Quantity) AS Total
        FROM food_listings
        GROUP BY Meal_Type;
    """,

    "Q17_Food_By_City": """
        SELECT Location,
            SUM(Quantity) AS Total_Food
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Food DESC;
    """,

    "Q18_Completed_Claims": """
        SELECT COUNT(*) AS Completed_Claims
        FROM claims
        WHERE Status='Completed';
    """,

    "Q19_Pending_Claims": """
        SELECT COUNT(*) AS Pending_Claims
        FROM claims
        WHERE Status='Pending';
    """,

    "Q20_Cancelled_Claims": """
        SELECT COUNT(*) AS Cancelled_Claims
        FROM claims
        WHERE Status='Cancelled';
    """

}