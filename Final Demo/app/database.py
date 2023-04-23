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



def get_all_flights():
    conn = db.connect()
    query_results = conn.execute("SELECT * FROM flights LIMIT 200;").fetchall()
    conn.close()

    flights = [dict(row) for row in query_results]
    return flights


def get_all_planes():
    conn = db.connect()
    query_results = conn.execute("SELECT * FROM planes;").fetchall()
    conn.close()

    planes = [dict(row) for row in query_results]
    return planes


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

    query = conn.execute(f"SELECT * FROM flights WHERE {query_conditions}", params)
    query_results = query.fetchall()
    conn.close()

    flights = [dict(row) for row in query_results]
    return flights


# def fetch_all_airport_ids():
#     conn = db.connect()
#     query_results = conn.execute("SELECT airportID FROM airports").fetchall()
#     conn.close()

#     airport_ids = [result[0] for result in query_results]
#     return airport_ids

# def update_cancellation_rate(airport_id):
#     conn = db.connect()
#     conn.execute("CALL update_cancellation_rate(%s)", (airport_id,))
#     conn.close()

# def update_all_cancellation_rates():
#     airport_ids = fetch_all_airport_ids()
#     for airport_id in airport_ids:
#         update_cancellation_rate(airport_id)



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



