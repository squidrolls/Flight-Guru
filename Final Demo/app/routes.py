""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
import pymysql
from flask import redirect
from flask import url_for
from flask import Flask, render_template, request, redirect, url_for, session



@app.route("/delete/<string:airlineID>", methods=['POST'])
def delete(airlineID):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(airlineID)
        result = {'success': True, 'response': 'Removed name'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/edit/<string:old_airlineID>", methods=['POST'])
def edit(old_airlineID):
    """ received post requests for entry updates """

    data = request.get_json()

    print("EDIT Data received:", data)  # For debugging

    try:
        db_helper.update_task_entry(old_airlineID, data["airlineID"], data["name"])  # Updated this line
        result = {'success': True, 'response': 'Task Updated'}
    except Exception as e:  # Catch the exception to print the error message
        print("Error:", e)  # For debugging
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ receives post requests to add new task """
    data = request.get_json()
    print("Create Data received:", data)  # For debugging
    try:
        db_helper.insert_new_task(data['airlineID'], data['name'])
        result = {'success': True, 'response': 'Task Created'}
    except Exception as e:  # Catch the exception to print the error message
        print("Error:", e)  # For debugging
        if isinstance(e, pymysql.err.IntegrityError) and e.args[0] == 1062:
            result = {'success': False, 'response': 'Duplicate entry, add rejected'}
        else:
            result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)




# @app.route("/")
# def homepage():
#     """ returns rendered homepage """
#     items = db_helper.fetch_todo()
#     return render_template("index.html", items=items)


@app.route('/airline')
def airline():
    airlines = db_helper.fetch_todo()
    return render_template('airline.html', items=airlines)

@app.route('/airline_delays')
def airline_delays():
    delays = db_helper.get_average_delays()
    return render_template('airline_delays.html', delays=delays)

# @app.route('/airport_cancelled_flights')
# def airport_cancelled_flights():
#     cancels = db_helper.get_cancelled_flights()
#     return render_template('airport_cancelled_flights.html', cancels=cancels)

# @app.route('/')
# def main():
#     return render_template('index.html')

@app.route('/airports')
def airports():
    airports_data = db_helper.fetch_airports()
    return render_template('airports.html', airports=airports_data)

@app.route('/flights')
def flights():
    flights = db_helper.get_all_flights()
    return render_template('flights.html', flights=flights)

@app.route('/delayed-flights')
def delays():
    delays = db_helper.get_all_delays()
    return render_template('delays.html', delays=delays)

@app.route('/search_flights', methods=['POST'])
def search_flights():
    airline = request.form.get('search_airline', '').strip()
    flight_number = request.form.get('search_flight_number', '').strip()
    search_date = request.form.get('search_date', '').strip()

    if airline or flight_number or search_date:
        flights = db_helper.search_flights_by_airline_flight_number_or_date(airline, flight_number, search_date)
    else:
        flights = db_helper.get_all_flights()

    return render_template('flights.html', flights=flights)

@app.route('/search_delays', methods=['POST'])
def search_delays():
    airline = request.form.get('search_airline', '').strip()
    flight_number = request.form.get('search_flight_number', '').strip()
    search_date = request.form.get('search_date', '').strip()

    if airline or flight_number or search_date:
        delays = db_helper.search_delays_by_airline_flight_number_or_date(airline, flight_number, search_date)
    else:
        delays = db_helper.get_all_delays()

    return render_template('delays.html', delays=delays)

@app.route('/search_subscribed_flights', methods=['POST'])
def search_subscribed_flights():
    airline = request.form.get('search_airline', '').strip()
    flight_number = request.form.get('search_flight_number', '').strip()
    search_date = request.form.get('search_date', '').strip()

    if airline or flight_number or search_date:
        flights = db_helper.search_flights_by_airline_flight_number_or_date(airline, flight_number, search_date)
    else:
        flights = db_helper.get_all_flights()

    return render_template('subscription.html', flights=flights)




@app.route('/planes')
def planes():
    planes = db_helper.get_all_planes()
    return render_template('planes.html', planes=planes)


# @app.route('/cancelled_flights_by_states', methods=['GET', 'POST'])
# def cancelled_flights_by_states():
#     if request.method == 'POST':
#         states = request.form.getlist('states')
#         cancelled_flights = db_helper.fetch_cancelled_flights_by_state(states)
        
#         return render_template('cancelled_flights_by_states.html', 
#                                 cancelled_flights=cancelled_flights, 
#                                 selected_states=states)
#     else:
#         # If it's a GET request, fetch all the data
#         cancelled_flights = db_helper.fetch_cancelled_flights_by_state([])

#         return render_template('cancelled_flights_by_states.html', 
#                                 cancelled_flights=cancelled_flights,
#                                 selected_states=None)


@app.route('/', methods=['GET', 'POST'])
def cancelled_flights_by_states():
    # # Call update_all_cancellation_rates() before fetching the data
    # db_helper.update_all_cancellation_rates()

    if request.method == 'POST':
        states = request.form.getlist('states')
        cancelled_flights = db_helper.fetch_cancelled_flights_by_state(states)
        print("Cancelled Flights Data1:", cancelled_flights)
        return render_template('index.html', cancelled_flights=cancelled_flights)
    else:
        cancelled_flights = db_helper.fetch_cancelled_flights_by_state([])
        print("Cancelled Flights Data2:", cancelled_flights)
        return render_template('index.html', cancelled_flights=cancelled_flights)





@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        status = db_helper.check_user_credentials(username, password)

        if status == 0: 
            session["user"] = username  #store the username
            return redirect(url_for("cancelled_flights_by_states"))
        elif status == 1:
            error_message = "User not found. Please sign up."
        elif status == 2:
            error_message = "Incorrect password. Please try again."

    return render_template("login.html", error_message=error_message)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        if db_helper.username_exists(username):
            return "Username already exists. Please choose a different one.", 409
        elif db_helper.create_user(username, password):
            return "User created successfully", 200
        else:
            return "Error creating user", 500

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("cancelled_flights_by_states"))


@app.route("/account_settings")
def account_settings():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("account_settings.html")


@app.route("/update_password", methods=["POST"])
def update_password():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    old_password = data["old_password"]
    new_password = data["new_password"]
    username = session["user"]

    status = db_helper.check_user_credentials(username, old_password)

    if status == 0:
        db_helper.update_user_password(username, new_password)
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Incorrect old password"}), 400

@app.route('/subscription')
def subscription():
    username = session.get('user')
    if username:
        subscribed_flights = db_helper.get_subscribed_flights(username)
        flights = db_helper.get_flights_with_cancellation_type_0()
        
        # Create a set of subscribed flight identifiers
        subscribed_flight_identifiers = {(flight['DATE'], flight['FLIGHT_NUMBER'], flight['AIRLINE']) for flight in subscribed_flights}

        return render_template('subscription.html', subscribed_flights=subscribed_flights, flights=flights, subscribed_flight_identifiers=subscribed_flight_identifiers)
    else:
        return redirect(url_for('login'))




@app.route('/subscribe_flight', methods=['POST'])
def subscribe_flight():
    username = session.get('user')
    if username:
        airline = request.form.get('airline')
        flight_number = request.form.get('flight_number')
        tail_number = request.form.get('tail_number')
        date = request.form.get('date')
        scheduled_departure = request.form.get('scheduled_departure')
        status = request.form.get('status')
        db_helper.add_subscription(username, airline, flight_number, tail_number, date, scheduled_departure, status)
        return redirect(url_for('subscription'))
    else:
        return redirect(url_for('login'))


@app.route('/unsubscribe_flight', methods=['POST'])
def unsubscribe_flight():
    username = session.get('user')
    if username:
        flight_number = request.form.get('flight_number')
        airline = request.form.get('airline')
        db_helper.remove_subscription(username, flight_number, airline)
        return redirect(url_for('subscription'))
    else:
        return redirect(url_for('login'))


