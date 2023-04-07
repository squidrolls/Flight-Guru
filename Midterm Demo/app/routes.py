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

    print("Data received:", data)  # For debugging

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
