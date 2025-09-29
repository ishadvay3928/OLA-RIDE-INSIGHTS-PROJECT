# 🚖 Ola Rides Insights Project

## 📌 Overview

📊 A Streamlit-based analytics dashboard integrated with SQLite and Power BI to analyze **ride patterns, cancellations, customer behavior, payments, and ratings**.
The app helps Ola optimize **driver allocation, reduce cancellations, improve customer satisfaction, and enhance operational efficiency**.

🔗 **Live App**: [Ola Ride Insights Streamlit App](https://ola-ride-insights.streamlit.app/)

---

## 🚀 Features

### 🔎 SQL Queries View

Pre-built SQL analyses including:

* Retrieve successful bookings
* Average ride distance by vehicle type
* Cancelled rides (Customer/Driver) with reasons
* Top 5 customers by rides & booking value
* Revenue from successful rides
* Incomplete rides with reasons

### 📊 BI Dashboard View

Interactive KPIs and visualizations:

* Ride volume over time
* Booking status breakdown
* Revenue by payment method
* Ride distance distribution per day
* Customer vs. Driver ratings
* Cancellation reasons (Customer & Driver)
* Top 5 customers by value

### 🎛️ Filters & Navigation

* Two navigations: **SQL Queries** & **BI Dashboard**
* Sections: **Overall, Vehicle Type, Revenue, Cancellation, Ratings**
* Interactive slicers for dynamic exploration

---

## 🗂️ Project Structure

```
Ola-Rides-Insights/
│── Ola_clean_dataset.csv              # cleaned CSV dataset
│── ola_rides.db                       # SQLite database
│── Ola_Ride_Insights.ipynb            # colab notebook for EDA & preprocessing
│── app.py                             # Streamlit application
│── Ola Ride Dashboard.pbix            # Power BI report
│── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## 🛠️ Installation & Setup

1️⃣ Clone the repository

```bash
git clone https://github.com/ishadvay3928/Ola-Rides-Insights.git
cd Ola-Rides-Insights
```

2️⃣ Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

4️⃣ Database setup

* The app uses **SQLite (`ola_rides.db`)** by default.
* If missing, place the processed dataset in `Ola_clean_dataset.csv` and recreate the DB using provided notebooks.

5️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📦 Requirements

`requirements.txt`

```
streamlit
sqlalchemy
pandas
plotly
```

---

## 📬 Contact

👩‍💻 **Isha Chaudhary**

📧 [ishachaudhary3928@gmail.com](mailto:ishachaudhary3928@gmail.com)

🔗 [LinkedIn](https://linkedin.com)

📍 Noida, India
