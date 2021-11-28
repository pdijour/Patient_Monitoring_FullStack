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
    connect("mongodb+srv://<userid>:<pswd>@bme547.ba348.mongodb.net/health_db"
            "?retryWrites=true&w=majority")
    print("Connection attempt finished.")
