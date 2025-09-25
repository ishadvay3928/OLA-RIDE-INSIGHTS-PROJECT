-- Create the table for Ola rides
CREATE TABLE IF NOT EXISTS ola_rides (
    ride_date TIMESTAMP,
    ride_time TIME,
    booking_id VARCHAR,
    booking_status VARCHAR,
    customer_id VARCHAR,
    vehicle_type VARCHAR,
    pickup_location VARCHAR,
    drop_location VARCHAR,
    v_tat NUMERIC,
    c_tat NUMERIC,
    canceled_rides_by_customer TEXT,
    canceled_rides_by_driver TEXT,
    incomplete_rides VARCHAR,
    incomplete_rides_reason TEXT,
    booking_value NUMERIC,
    payment_method VARCHAR,
    ride_distance NUMERIC,
    driver_ratings NUMERIC,
    customer_rating NUMERIC
);

-- Load data from CSV
COPY ola_rides (
    ride_date,
    ride_time,
    booking_id,
    booking_status,
    customer_id,
    vehicle_type,
    pickup_location,
    drop_location,
    v_tat,
    c_tat,
    canceled_rides_by_customer,
    canceled_rides_by_driver,
    incomplete_rides,
    incomplete_rides_reason,
    booking_value,
    payment_method,
    ride_distance,
    driver_ratings,
    customer_rating
)
FROM 'D:/DOCUMENTS/DATA ANALYTICS PROJECTS/Ola Ride Insights Project/Ola_clean_dataset.csv'
DELIMITER ',' CSV HEADER;

select * from ola_rides;


-- queries

-- 1. Retrieve all successful bookings:
select * from ola_rides
where Booking_Status = 'Success';

-- 2. Find the average ride distance for each vehicle type:
SELECT vehicle_type, ROUND(AVG(ride_distance),2) AS avg_distance 
FROM ola_rides WHERE Booking_Status = 'Success' GROUP BY vehicle_type;

-- 3. Get the total number of cancelled rides by customers:
select count(*) from ola_rides 
where Booking_Status = 'Canceled by Customer';

-- 4. List the top 5 customers who booked the highest number of rides:
select Customer_ID, count(Booking_ID) as Total_Rides 
from ola_rides
group by Customer_ID
Order By Total_Rides Desc limit 5;

-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues:
select count(*) from ola_rides where canceled_rides_by_driver = 'Personal & Car related issue';

-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
select max(Driver_Ratings) as Maximum_rating, MIN(driver_ratings) AS min_rating
from ola_rides where Vehicle_Type = 'Prime Sedan';

-- 7. Retrieve all rides where payment was made using UPI:
select * from ola_rides where Payment_Method = 'UPI';

-- 8. Find the average customer rating per vehicle type:
select Vehicle_Type, avg(Customer_Rating) as Average_customer_rating from ola_rides
group by Vehicle_Type;

-- 9. Calculate the total booking value of rides completed successfully:
select sum(Booking_Value) as total_sucessful_value from ola_rides where Booking_Status = 'Success'; 

-- 10. List all incomplete rides along with the reason:
select Incomplete_Rides,Incomplete_Rides_Reason from ola_rides where Incomplete_Rides = 'Yes';