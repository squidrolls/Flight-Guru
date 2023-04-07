"""Defines all the functions related to the database"""
from app import db

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

    Returns:
        None
    """

    conn = db.connect()
    
    if old_airlineID != new_airlineID:
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
