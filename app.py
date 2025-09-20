import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
import plotly.express as px

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(page_title="Ola Ride Dashboard", layout="wide")

# --------------------
# DB CONNECTION
# --------------------
DB_FILE = "ola_rides.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False, connect_args={"check_same_thread": False})

@st.cache_data(ttl=60)
def q(sql, params=None):
    with engine.connect() as conn:
        if params:
            return pd.read_sql(text(sql), conn, params=params)
        return pd.read_sql(text(sql), conn)

def exec_write(sql, params=None):
    with engine.begin() as conn:
        conn.execute(text(sql), params or {})

# --------------------
# LOAD CSV IF EMPTY
# --------------------
def load_csv_if_empty(table_name, csv_file):
    try:
        count = q(f"SELECT COUNT(*) AS cnt FROM {table_name}")["cnt"][0]
    except Exception:
        count = 0
    if count == 0 and os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df.columns = [c.lower() for c in df.columns]
        df.to_sql(table_name, engine, if_exists="append", index=False)
        st.info(f"📥 Loaded {table_name} from {csv_file} ({len(df)} rows)")

# Example (replace with your Ola dataset CSV)
csv_files = {"ola_rides": "ola_clean_dataset.csv"}
for table, file in csv_files.items():
    load_csv_if_empty(table, file)

# --------------------
# SIDEBAR NAVIGATION
# --------------------
st.sidebar.title("🚖 Ola Ride Insights")
page = st.sidebar.radio("Navigation", ["SQL Queries View", "BI Dashboard View"])

# --------------------
# PAGE 1: SQL INSIGHTS
# --------------------
if page == "SQL Queries View":
    st.header("🔎 SQL Queries")

    query_map = {
        "1. Retrieve all successful bookings":
            "SELECT * FROM ola_rides WHERE booking_status = 'Success';",

        "2. Find the average ride distance for each vehicle type":
            "SELECT vehicle_type, ROUND(AVG(ride_distance),2) AS avg_distance FROM ola_rides GROUP BY vehicle_type;",

        "3. Get the total number of cancelled rides by customers":
            "select count(*) from ola_rides where Booking_Status = 'Canceled by Customer';",

        "4. List the top 5 customers who booked the highest number of rides":
               """select Customer_ID, count(Booking_ID) as Total_Rides 
                  from ola_rides
                  group by Customer_ID
                  Order By Total_Rides Desc limit 5;""",

        "5. Get the number of rides cancelled by drivers due to personal and car-related issues":
            "select count(*) from ola_rides where canceled_rides_by_driver = 'Personal & Car related issue';""",

        "6. Find the maximum and minimum driver ratings for Prime Sedan bookings":
            "select max(Driver_Ratings) as Maximum_rating, MIN(driver_ratings) AS min_rating from ola_rides where Vehicle_Type = 'Prime Sedan';",
            
        "7. Retrieve all rides where payment was made using UPI":   
            "select * from ola_rides where Payment_Method = 'UPI';",

        "8. Find the average customer rating per vehicle type":
            "select Vehicle_Type, avg(customer_Rating) as avg_customer_rating from ola_rides group by Vehicle_Type;",

        "9. Calculate the total booking value of rides completed successfully":
            "select sum(Booking_Value) as total_sucessful_value from ola_rides where Booking_Status = 'Success';",

        "10. List all incomplete rides along with the reason":
            "select Incomplete_Rides,Incomplete_Rides_Reason from ola_rides where Incomplete_Rides = 'Yes';"
    }

    chosen = st.selectbox("Choose SQL Query", list(query_map.keys()))
    df = q(query_map[chosen])
    st.dataframe(df, use_container_width=True)

# --------------------
# PAGE 2: POWER BI-LIKE VISUALS INSIDE STREAMLIT
# --------------------
elif page == "BI Dashboard View":
    st.header("📊 Ola Ride BI Dashboard")

    section = st.selectbox("Choose Section", ["Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"])

    df = pd.read_csv("D:\DOCUMENTS\DATA ANALYTICS PROJECTS\Ola Ride Insights Project\Ola_clean_dataset.csv")

    # ---------------- OVERALL ----------------
    if section == "Overall":
     total_bookings = len(df)
     total_value = df.drop_duplicates(subset="Booking_ID")["Booking_Value"].sum()

    # ✅ Successful booking value
     success_value = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()

     col1, col2, col3 = st.columns(3)
     col1.metric("Total Bookings", f"{total_bookings:,}")
     col2.metric("Total Booking Value", f"{total_value/1_000_000:.1f}M")
     col3.metric("Successful Booking Value", f"{success_value/1_000_000:.1f}M")

    # Pie chart for Booking Status
     df_status = df["Booking_Status"].value_counts().reset_index()
     df_status.columns = ["status", "count"]
     fig1 = px.pie(df_status, names="status", values="count", title="Booking Status Breakdown")
     st.plotly_chart(fig1, use_container_width=True)

     # Ride Volume Over Time (cumulative) 
     df_time = df.groupby("Date")["Booking_ID"].count().reset_index() 
     df_time.rename(columns={"Booking_ID": "daily_count"}, inplace=True) 
     df_time["booking_count"] = df_time["daily_count"].cumsum() 
     fig2 = px.line(df_time, x="Date", y="booking_count", title="Ride Volume Over Time") 
     fig2.update_traces(line_color="black") 
     fig2.update_layout(yaxis_title="Booking Count", xaxis_title="Date", template="simple_white") 
     st.plotly_chart(fig2, use_container_width=True)
     
    # ---------------- VEHICLE TYPE ----------------
    elif section == "Vehicle Type":
        df_vehicle = df.groupby("Vehicle_Type").agg(
            total_value=("Booking_Value", "sum"),
            success_value=("Booking_Value", lambda x: df.loc[x.index][df.loc[x.index]["Booking_Status"]=="Success"]["Booking_Value"].sum()),
            avg_distance=("Ride_Distance", "mean"),
            total_distance=("Ride_Distance", "sum")
        ).reset_index()

        st.dataframe(df_vehicle, use_container_width=True)

        fig = px.bar(df_vehicle, x="Vehicle_Type", y="avg_distance", title="Avg Distance Travelled by Vehicle Type")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- REVENUE ----------------
    elif section == "Revenue":
        df_payment = df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
        fig3 = px.bar(df_payment, x="Payment_Method", y="Booking_Value", title="Revenue by Payment Method")
        st.plotly_chart(fig3, use_container_width=True)

        df_top5 = df.groupby("Customer_ID")["Booking_Value"].sum().reset_index().sort_values(by="Booking_Value", ascending=False).head(5)
        st.subheader("Top 5 Customers by Total Booking Value")
        st.dataframe(df_top5)

        df_distance = df.groupby("Date")["Ride_Distance"].sum().reset_index()
        fig4 = px.bar(df_distance, x="Date", y="Ride_Distance", title="Ride Distance Distribution Per Day")
        st.plotly_chart(fig4, use_container_width=True)

    # ---------------- CANCELLATION ----------------
    elif section == "Cancellation":
        total = len(df)
        success = (df["Booking_Status"] == "Success").sum()
        cancelled = total - success
        rate = cancelled / total * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Bookings", f"{total:,}")
        col2.metric("Succeeded", f"{success:,}")
        col3.metric("Cancelled", f"{cancelled:,}")
        col4.metric("Cancellation Rate", f"{rate:.2f}%")

        # Cancelled by Customer
        df_cust = df[df["Booking_Status"] == "Canceled by Customer"]["Canceled_Rides_by_Customer"].value_counts(dropna=True).reset_index()
        df_cust.columns = ["Reason", "Count"]
        if not df_cust.empty:
            fig5 = px.pie(df_cust, names="Reason", values="Count", title="Cancelled Rides Reasons (Customer)")
            st.plotly_chart(fig5, use_container_width=True)

        # Cancelled by Driver
        df_driver = df[df["Booking_Status"] == "Canceled by Driver"]["Canceled_Rides_by_Driver"].value_counts(dropna=True).reset_index()
        df_driver.columns = ["Reason", "Count"]
        if not df_driver.empty:
            fig6 = px.pie(df_driver, names="Reason", values="Count", title="Cancelled Rides Reasons (Driver)")
            st.plotly_chart(fig6, use_container_width=True)

    # ---------------- RATINGS ----------------
    elif section == "Ratings":
        df_ratings = df.groupby("Vehicle_Type").agg(
            Driver_Avg=("Driver_Ratings", "mean"),
            Customer_Avg=("Customer_Rating", "mean")
        ).reset_index()

        st.subheader("Driver Ratings by Vehicle Type")
        fig7 = px.bar(df_ratings, x="Vehicle_Type", y="Driver_Avg", title="Driver Ratings")
        st.plotly_chart(fig7, use_container_width=True)

        st.subheader("Customer Ratings by Vehicle Type")
        fig8 = px.bar(df_ratings, x="Vehicle_Type", y="Customer_Avg", title="Customer Ratings")
        st.plotly_chart(fig8, use_container_width=True)
