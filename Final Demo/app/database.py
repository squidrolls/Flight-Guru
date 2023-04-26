"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text


def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from airline;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "airlineID": result[0],
            "name": result[1],
            # "status": result[2]
        }
        todo_list.append(item)

    return todo_list

def update_task_entry(old_airlineID: str, new_airlineID: str, name: str) -> None:
    """Updates task description based on given `old_airlineID`

    Args:
        old_airlineID (str): The old airline ID
        new_airlineID (str): The new airline ID
        name (str): Updated name
    """
    conn = db.connect()
    
    if old_airlineID != new_airlineID :
        # Update the airline ID and the name
        query = 'UPDATE airline SET airlineID = "{}", name = "{}" WHERE airlineID = "{}";'.format(new_airlineID, name, old_airlineID)
    else:
        # Only update the name
        query = 'UPDATE airline SET name = "{}" WHERE airlineID = "{}";'.format(name, old_airlineID)
    
    conn.execute(query)
    conn.close()

def insert_new_task(airlineID: str, name: str) -> None:
    conn = db.connect()
    query = 'INSERT INTO airline (airlineID, name) VALUES (%s, %s);'
    conn.execute(query, (airlineID, name))
    conn.close()

def remove_task_by_id(airlineID: str) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    # query = 'Delete From airline where airlineID={};'.format(airlineID)
    # conn.execute(query)
    query = "DELETE FROM airline WHERE airlineID=%s;"
    conn.execute(query, (airlineID,))
    conn.close()


def get_average_delays():
    conn = db.connect()
    query = '''
        SELECT a.name as "Airline", avg(d.AIR_SYSTEM_DELAY + d.SECURITY_DELAY + d.AIRLINE_DELAY + d.LATE_AIRCRAFT_DELAY + d.WEATHER_DELAY) as "Average Delay"
        FROM delays d JOIN airline a ON (d.AIRLINE = a.airlineID)
        GROUP BY (a.airlineID)
        LIMIT 15;
    '''
    result = conn.execute(query)
    conn.close()
    return result.fetchall()

# def get_cancelled_flights():
#     conn = db.connect()
#     query = '''
#         SELECT a.AIRPORT, COUNT(f.CANCELLATION_TYPE) as "Number of Cancelled Flights"
#         FROM flights f
#         JOIN airports a ON (f.ORIGIN_AIRPORT = a.airportID)
#         WHERE f.CANCELLATION_TYPE != '0'
#         GROUP BY a.airportID
#         ORDER BY COUNT(*) DESC
#         LIMIT 15;
#     '''
#     result = conn.execute(query)
#     conn.close()
#     return result.fetchall()

def get_cancelled_flights_by_states(states: list):
    conn = db.connect()
    
    # Convert the list of states to a comma-separated string of single-quoted state abbreviations
    states_string = ', '.join(f"'{state}'" for state in states)

    query = '''
        SELECT a.AIRPORT, a.STATE, COUNT(f.CANCELLATION_TYPE) as "Number of Cancelled Flights"
        FROM flights f
        JOIN airports a ON (f.ORIGIN_AIRPORT = a.airportID)
        WHERE a.STATE IN ({states_string}) AND f.CANCELLATION_TYPE != '0'
        GROUP BY a.airportID
        ORDER BY COUNT(*) DESC
        LIMIT 50;
    '''
    
    query_results = conn.execute(query).fetchall()
    conn.close()

    cancelled_flights = [dict(row) for row in query_results]
    return cancelled_flights


def fetch_airports() -> list:
    conn = db.connect()
    query_results = conn.execute("SELECT * FROM airports;").fetchall()
    conn.close()

    airports_list = []
    for result in query_results:
        airport = {
            "airportID": result[0],
            "AIRPORT": result[1],
            "CITY": result[2],
            "STATE": result[3],
            "COUNTRY": result[4],
            "LATITUDE": result[5],
            "LONGITUDE": result[6],

        }
        airports_list.append(airport)

    return airports_list


def get_all_planes():
    conn = db.connect()
    query_results = conn.execute("SELECT * FROM planes;").fetchall()
    conn.close()

    planes = [dict(row) for row in query_results]
    return planes


def get_all_flights():
    conn = db.connect()
    query_results = conn.execute("""
        SELECT DATE, AIRLINE, FLIGHT_NUMBER, TAIL_NUMBER,ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL, cancellations.status as CANCELLATION_REASON
        FROM flights
        LEFT JOIN cancellations ON flights.CANCELLATION_TYPE = cancellations.type
        LIMIT 200;
    """).fetchall()
    conn.close()

    flights = [dict(row) for row in query_results]
    return flights

def get_all_delays():
    conn = db.connect()
    query_results = conn.execute("""
        SELECT *
        FROM delays
        LIMIT 200;""").fetchall()
    conn.close()

    delays = [dict(row) for row in query_results]
    return delays

def search_flights_by_airline_flight_number_or_date(airline, flight_number, search_date):
    conn = db.connect()

    conditions = []
    params = []

    if airline:
        conditions.append("AIRLINE = %s")
        params.append(airline)

    if flight_number:
        conditions.append("FLIGHT_NUMBER = %s")
        params.append(flight_number)

    if search_date:
        conditions.append("DATE = %s")
        params.append(search_date)

    query_conditions = " AND ".join(conditions)

    query = conn.execute(f"""
        SELECT DATE, AIRLINE, FLIGHT_NUMBER, TAIL_NUMBER,ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL, cancellations.status as CANCELLATION_REASON
        FROM flights
        LEFT JOIN cancellations ON flights.CANCELLATION_TYPE = cancellations.type
        WHERE {query_conditions}
    """, params)
    query_results = query.fetchall()
    conn.close()

    flights = [dict(row) for row in query_results]
    return flights

def search_delays_by_airline_flight_number_or_date(airline, flight_number, search_date):
    conn = db.connect()

    conditions = []
    params = []

    if airline:
        conditions.append("AIRLINE = %s")
        params.append(airline)

    if flight_number:
        conditions.append("FLIGHT_NUMBER = %s")
        params.append(flight_number)

    if search_date:
        conditions.append("DATE = %s")
        params.append(search_date)

    query_conditions = " AND ".join(conditions)

    query = conn.execute(f"""
        SELECT *
        FROM delays
        WHERE {query_conditions}
    """, params)
    query_results = query.fetchall()
    conn.close()

    delays = [dict(row) for row in query_results]
    return delays





#mapping
# def fetch_cancelled_flights_by_state(states=None):
#     conn = db.connect()

#     if states:
#         query = '''
#                 WITH flight_counts AS (
#                     SELECT f.ORIGIN_AIRPORT as airportID,
#                         COUNT(*) as total_flights,
#                         SUM(CASE WHEN f.CANCELLATION_TYPE != '0' THEN 1 ELSE 0 END) as cancelled_flights
#                     FROM flights f
#                     JOIN airports a ON f.ORIGIN_AIRPORT = a.airportID
#                     WHERE a.STATE IN :states
#                     GROUP BY f.ORIGIN_AIRPORT
#                 )
#                 SELECT a.AIRPORT, a.STATE, a.LATITUDE, a.LONGITUDE,
#                     fc.cancelled_flights as "Number of Cancelled Flights",
#                     (fc.cancelled_flights * 100) / fc.total_flights as "Cancellation Rate"
#                 FROM airports a
#                 JOIN flight_counts fc ON a.airportID = fc.airportID
#                 ORDER BY fc.cancelled_flights DESC


#         '''
#         query_results = conn.execute(text(query), states=tuple(states)).fetchall()
#     else:
#         query = '''
#                     WITH flight_counts AS (
#                         SELECT f.ORIGIN_AIRPORT as airportID,
#                             COUNT(*) as total_flights,
#                             SUM(CASE WHEN f.CANCELLATION_TYPE != '0' THEN 1 ELSE 0 END) as cancelled_flights
#                         FROM flights f
#                         JOIN airports a ON f.ORIGIN_AIRPORT = a.airportID
#                         GROUP BY f.ORIGIN_AIRPORT
#                     )
#                     SELECT a.AIRPORT, a.STATE, a.LATITUDE, a.LONGITUDE,
#                         fc.cancelled_flights as "Number of Cancelled Flights",
#                         (fc.cancelled_flights * 100) / fc.total_flights as "Cancellation Rate"
#                     FROM airports a
#                     JOIN flight_counts fc ON a.airportID = fc.airportID
#                     ORDER BY fc.cancelled_flights DESC

#         '''
#         query_results = conn.execute(text(query)).fetchall()

#     conn.close()

#     cancelled_flights = []
#     for result in query_results:
#         flight = {
#             "AIRPORT": result[0],
#             "STATE": result[1],
#             "LATITUDE": result[2],
#             "LONGITUDE": result[3],
#             "Number of Cancelled Flights": float(result[4]),
#             "Cancellation Rate": float(result[5]),
#         }
#         cancelled_flights.append(flight)

#     return cancelled_flights


def fetch_cancelled_flights_by_state(states=None):
    conn = db.connect()

    if states:
        query = '''
                SELECT a.AIRPORT, a.STATE, a.LATITUDE, a.LONGITUDE,
                    acr.cancelled_flights as "Number of Cancelled Flights",
                    acr.cancellation_rate as "Cancellation Rate"
                FROM airports a
                JOIN airport_cancellation_rates acr ON a.airportID = acr.airportID
                WHERE a.STATE IN :states
                ORDER BY acr.cancelled_flights DESC
        '''
        query_results = conn.execute(text(query), states=tuple(states)).fetchall()
    else:
        query = '''
                SELECT a.AIRPORT, a.STATE, a.LATITUDE, a.LONGITUDE,
                    acr.cancelled_flights as "Number of Cancelled Flights",
                    acr.cancellation_rate as "Cancellation Rate"
                FROM airports a
                JOIN airport_cancellation_rates acr ON a.airportID = acr.airportID
                ORDER BY acr.cancelled_flights DESC
        '''
        query_results = conn.execute(text(query)).fetchall()

    conn.close()

    cancelled_flights = []
    for result in query_results:
        flight = {
            "AIRPORT": result[0],
            "STATE": result[1],
            "LATITUDE": result[2],
            "LONGITUDE": result[3],
            "Number of Cancelled Flights": int(result[4]),
            "Cancellation Rate": float(result[5]),
        }
        cancelled_flights.append(flight)

    return cancelled_flights








def get_user_password(username: str):
    conn = db.connect()
    query_results = conn.execute(text("SELECT password FROM users WHERE username = :username"), {'username': username}).fetchone()
    conn.close()
    if query_results:
        return query_results[0]
    return None


def check_user_credentials(username, password) -> int:
    conn = db.connect()
    query = "SELECT password FROM users WHERE username = :username"
    result = conn.execute(text(query), {"username": username}).fetchone()
    conn.close()

    if result is None:
        return 1  # User not found
    elif result[0] == password:
        return 0  # Correct credentials
    else:
        return 2  # Incorrect password


def update_user_password(username: str, new_password: str):
    conn = db.connect()
    query = text("UPDATE users SET password = :new_password WHERE username = :username")
    conn.execute(query, {"username": username, "new_password": new_password})
    conn.close()


def create_user(username: str, password: str) -> bool:
    conn = db.connect()
    try:
        conn.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"), {'username': username, 'password': password})
        conn.close()
        return True
    except:
        conn.close()
        return False

def username_exists(username: str) -> bool:
    """Checks if a given username already exists in the database
    """
    conn = db.connect()
    result = conn.execute(text("SELECT COUNT(*) FROM users WHERE username = :username"), {'username': username}).scalar()
    conn.close()

    return result > 0


def get_flights_with_cancellation_type_0():
    conn = db.connect()
    query_results = conn.execute("""
        SELECT DATE, AIRLINE, FLIGHT_NUMBER, TAIL_NUMBER,ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL,cancellations.status as CANCELLATION_REASON
        FROM flights
        LEFT JOIN cancellations ON flights.CANCELLATION_TYPE = cancellations.type
        WHERE CANCELLATION_TYPE = 0
        LIMIT 200;
    """).fetchall()
    conn.close()

    flights = [dict(row) for row in query_results]
    return flights




def add_subscription(username, airline, flight_number, tail_number, date, scheduled_departure, status):
    conn = db.connect()
    conn.execute(
        "INSERT INTO subscription (username, airline, flight_number, tail_number, date, scheduled_departure, status) VALUES (%s, %s, %s, %s, %s, %s, %s);",
        (username, airline, flight_number, tail_number, date, scheduled_departure, status)
    )
    
    conn.close()


def get_subscribed_flights(username):
    conn = db.connect()
    query_results = conn.execute("""
        SELECT f.DATE, f.AIRLINE, f.FLIGHT_NUMBER, f.TAIL_NUMBER, f.SCHEDULED_DEPARTURE, f.SCHEDULED_ARRIVAL, cancellations.status as STATUS
        FROM flights f
        JOIN subscription ON (f.FLIGHT_NUMBER = subscription.flight_number AND f.AIRLINE = subscription.airline AND f.DATE=subscription.date)
        LEFT JOIN cancellations ON f.CANCELLATION_TYPE = cancellations.type
        WHERE subscription.username = %s;
    """, (username,)).fetchall()
    conn.close()

    flights = [dict(row) for row in query_results]
    return flights




def remove_subscription(username, flight_number, airline):
    conn = db.connect()
    conn.execute(
        "DELETE FROM subscription WHERE username = %s AND flight_number = %s AND airline = %s;",
        (username, flight_number, airline)
    )
    conn.close()


def search_user_subscribed_flights_by_airline_flight_number_or_date(username, airline, flight_number, search_date):
    conn = db.connect()

    conditions = []
    params = [username]

    if airline:
        conditions.append("AIRLINE = %s")
        params.append(airline)

    if flight_number:
        conditions.append("FLIGHT_NUMBER = %s")
        params.append(flight_number)

    if search_date:
        conditions.append("DATE = %s")
        params.append(search_date)

    query_conditions = " AND ".join(conditions)

    query = conn.execute(f"""
        SELECT DATE, AIRLINE, FLIGHT_NUMBER, TAIL_NUMBER,ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL,cancellations.status as CANCELLATION_REASON
        FROM flights
        LEFT JOIN cancellations ON flights.CANCELLATION_TYPE = cancellations.type
        WHERE CANCELLATION_TYPE = 0 AND {query_conditions}
    """, params)

    query_results = query.fetchall()
    conn.close()

    subscribed_flights = [dict(row) for row in query_results]
    return subscribed_flights
