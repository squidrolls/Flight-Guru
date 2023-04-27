# 411 final demo 4.24 update


During the demo, the team should also discuss the following points: 

1. Explain your choice for the advanced database program and how it is suitable for your application. For example, if you chose a stored procedure+trigger, explain how this choice is suitable for your application.
2. How did the creative element add extra value to your application?
3. How would you want to further improve your application? In terms of database design and system optimization?
   - Currently, our application focuses on the user side. In the future, we plan to add an admin side, allowing administrators to manage flight data directly through the front-end interface, rather than relying on MySQL Workbench.
4. What were the challenges you faced when implementing and designing the application? How was it the same/different from the original design?
   - Changes in the subscription table design:
     - We designed the username as the primary key. However, during the implementation, we realized that a single user could subscribe to multiple flights, resulting in duplicate primary keys. To resolve this issue, we changed the primary key to an auto-incrementing number.
5. If you were to include a NoSQL database, how would you incorporate it into your application?

---

### Basic function:

1. Create, Read, Update, Delete ()
2. search operations 
   1. Flight table - could search by either 1 or 2 or 3 conditions
   2. Airport table - an **autocomplete** search.
   3. "Reset" button. When clicked, this button will clear the search input and display all the rows in the table again.
3. advanced query (description on two advanced query)

---

### Creative Function 1 - User login/signup function

1. Log in
   1. If the username and password are correct, the user is granted access to the application and redirected to the main page. 
   2. If the username is not found in the database, the user is notified to sign up. 
   3. If the password is incorrect, the user is asked to re-enter their password.
2. Sign up 
   1. Check if the username already exists in the database and notify the user with the message "Username already exists. Please choose a different one."
   2. The user is redirected to the login page.
3. After Login
   1. Show the username in the top-right corner.
   2. User could go to the account setting to change the password. (**Update** the database)
      1. If the user type wrong old password, display the error message.
      2. else, change the password.
   3. user could add subscription.
4. Log out function

### Procedure/Trigger and Creative function 2 - **Interactive Map Visualization**

1. Display airports as markers on the map, and users can click on the markers to see more details about the airport and its cancellations.

2. Allow users to **select specific states** to view the number of cancelled flights.

3. Modify the advanced SQL query to include the latitude and longitude for each airport, enabling their display on the map..

4. Generate Google map API.

5. Use a red icon to represent airports with a **cancellation rate** over 5% and a blue icon for airports with a cancellation rate below 5%.

6. Info window will automatically close after being open for 2 seconds.

7. **Challenge**: The query execution time is long due to the calculation of flight cancellation rate, which involves a nested **subquery**, and the flights table is very large.

   ```sql
   /*before*/
   SELECT a.AIRPORT, a.STATE, a.LATITUDE, a.LONGITUDE, 
          COUNT(f.CANCELLATION_TYPE) as "Number of Cancelled Flights",
          COUNT(f.CANCELLATION_TYPE) * 100 / (SELECT COUNT(*) FROM flights f2 WHERE f2.ORIGIN_AIRPORT = a.airportID) as "Cancellation Rate"
   FROM flights f
   JOIN airports a ON (f.ORIGIN_AIRPORT = a.airportID)
   WHERE f.CANCELLATION_TYPE != '0' AND a.STATE IN :states
   GROUP BY a.airportID
   ORDER BY COUNT(*) DESC
   ```

   To optimize query performance:

   1. Create **indexes** on columns used in the WHERE and JOIN clauses. Indexes can speed up searches and lookups.

      1. Create indexes for the “flights” and “airports” tables.
      2. Decrease the query time for all states from over 120 seconds to **30 seconds**.
      3. Still very **slow**. 

   2. Use a stored **procedure** and **trigger** to precompute and store the cancellation rate of each airport, which helps reduce the calculation time when retrieving the cancellation rate later.

      1. create a table to store the cancellation rates for each airport:

         ```sql
         CREATE TABLE airport_cancellation_rates (
             airportID varchar(45) PRIMARY KEY,
             cancelled_flights INT,
             cancellation_rate DECIMAL(5, 2)
         );
         ```

      2. Then, create a stored procedure to update the cancellation rate for a given airport:

         ```sql
         DROP PROCEDURE IF EXISTS update_cancellation_rate;
         DELIMITER //
         CREATE PROCEDURE update_cancellation_rate(IN airport_id VARCHAR(45))
         BEGIN
             DECLARE total_flights INT DEFAULT 0;
             DECLARE cancelled_flights INT DEFAULT 0;
         
             SELECT COUNT(*)
             INTO total_flights
             FROM flights
             WHERE ORIGIN_AIRPORT = airport_id;
         
             SELECT COUNT(*)
             INTO cancelled_flights
             FROM flights
             WHERE ORIGIN_AIRPORT = airport_id AND CANCELLATION_TYPE != '0';
             
              SET @cancellation_rate = (cancelled_flights * 100) / total_flights;
         
             INSERT INTO airport_cancellation_rates (airportID, cancelled_flights, cancellation_rate)
             VALUES (airport_id, cancelled_flights, @cancellation_rate)
             ON DUPLICATE KEY UPDATE
                 cancelled_flights = VALUES(cancelled_flights),
                 cancellation_rate = VALUES(cancellation_rate);
         END //
         DELIMITER ;
         ```

      3. Create two triggers that call the stored procedure whenever a new flight is inserted or updated:

         ```sql
         DELIMITER //
         CREATE TRIGGER update_cancellation_rate_after_insert
         AFTER INSERT ON flights
         FOR EACH ROW
         BEGIN
             CALL update_cancellation_rate(NEW.ORIGIN_AIRPORT);
         END //
         DELIMITER ;
         
         DELIMITER //
         CREATE TRIGGER update_cancellation_rate_after_update
         AFTER UPDATE ON flights
         FOR EACH ROW
         BEGIN
             CALL update_cancellation_rate(NEW.ORIGIN_AIRPORT);
             IF OLD.ORIGIN_AIRPORT <> NEW.ORIGIN_AIRPORT THEN
                 CALL update_cancellation_rate(OLD.ORIGIN_AIRPORT);
             END IF;
         END //
         DELIMITER ;
         ```

      4. Calculate the cancellation rates and insert them into **`airport_cancellation_rates`** table:

         ```sql
         INSERT INTO airport_cancellation_rates (airportID, cancelled_flights, cancellation_rate)
         WITH flight_counts AS (
             SELECT f.ORIGIN_AIRPORT as airportID,
                 COUNT(*) as total_flights,
                 SUM(CASE WHEN f.CANCELLATION_TYPE != '0' THEN 1 ELSE 0 END) as cancelled_flights
             FROM flights f
             GROUP BY f.ORIGIN_AIRPORT
         )
         SELECT fc.airportID,
             fc.cancelled_flights,
             (fc.cancelled_flights * 100) / fc.total_flights as cancellation_rate
         FROM flight_counts fc
         ON DUPLICATE KEY UPDATE 
             cancelled_flights = fc.cancelled_flights,
             cancellation_rate = (fc.cancelled_flights * 100) / fc.total_flights;
         ```

      5. Now, whenever a new flight is inserted or an existing flight is updated, the cancellation rate for the affected airports will be automatically recalculated and stored in the **`airport_cancellation_rate`**table. 

      6. the sql query for the map visualization is as follow:

         ```sql
         /*after*/
         SELECT a.AIRPORT, a.STATE, a.LATITUDE, a.LONGITUDE,
         			 acr.cancelled_flights as "Number of Cancelled Flights",
         			 acr.cancellation_rate as "Cancellation Rate"
         FROM airports a
         JOIN airport_cancellation_rates acr ON a.airportID = acr.airportID
         WHERE a.STATE IN :states
         ORDER BY acr.cancelled_flights DESC
         ```

## Extra function:

1. Subscription function
   - Users can subscribe to flights by clicking the "Subscribe" button (update function)
   - the button will be disabled for flights they have already subscribed to.
   - Users can also remove their subscription by clicking the "Unsubscribe" button. (remove function)
   - If a subscribed flight gets cancelled, the flight status will be displayed in red.
2. Flight table
   - join the cancellations table to see the flight cancellation reason.
   - if a flight is cancelled, its text color in the **`CANCELLATION_REASON`**
     column will be displayed in red.
   - format the SCHEDULED_DEPARTURE and SCHEDULED_ARRIVAL columns as time
