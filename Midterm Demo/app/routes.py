""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

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
def update(old_airlineID):
    """ received post requests for entry updates """

    data = request.get_json()

    print("UPDATE Data received:", data)  # For debugging

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
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    return render_template("index.html", items=items)




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

@app.route('/cancelled_flights_by_states', methods=['GET', 'POST'])
def cancelled_flights_by_states():
    if request.method == 'POST':
        states = request.form.getlist('states')
        cancelled_flights = db_helper.get_cancelled_flights_by_states(states)
        return render_template('cancelled_flights_by_states.html', cancelled_flights=cancelled_flights, selected_states=states)
    return render_template('cancelled_flights_by_states.html')


# @app.route('/cancelled_flights_by_states', methods=['POST'])
# def cancelled_flights_by_states():
#     states = request.form.getlist('states[]')
#     cancelled_flights = db_helper.get_cancelled_flights_by_states(states)
#     return render_template('cancelled_flights_by_states.html', cancelled_flights=cancelled_flights)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/airports')
def airports():
    airports_data = db_helper.fetch_airports()
    return render_template('airports.html', airports=airports_data)

@app.route('/flights')
def flights():
    flights = db_helper.get_all_flights()
    return render_template('flights.html', flights=flights)

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



@app.route('/planes')
def planes():
    planes = db_helper.get_all_planes()
    return render_template('planes.html', planes=planes)