# cloud_server.py

import pymodm.errors
from flask import Flask, request, jsonify
import logging
from pymodm import connect, MongoModel, fields
from database_definitions import Patient

app = Flask(__name__)


def initialize_server():
    """ Initializes server conditions

    This function initializes the server log as well as creates a connection
    with the MongoDB database.
    """
    logging.basicConfig(filename="health_db_server.log", level=logging.DEBUG)
    print("Connecting to MongoDB...")
    connect("mongodb+srv://pdijour:bme547mongo@bme547.ba348.mongodb.net/"
            "final_project?retryWrites=true&w=majority")
    print("Connection attempt finished.")


@app.route("/", methods=["GET"])
def status():
    """Used to indicate that the server is running
    """
    return "Server is on"


if __name__ == '__main__':
    initialize_server()
    app.run()
