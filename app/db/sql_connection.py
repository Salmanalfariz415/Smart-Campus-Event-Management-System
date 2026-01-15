import mysql.connector
from dotenv import load_dotenv
load_dotenv()

import os

def get_sql_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="campus_event_system"
    )
    return connection