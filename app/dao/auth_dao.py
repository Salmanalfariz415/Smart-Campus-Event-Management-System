import mysql.connector
import jwt
from dotenv import load_dotenv
import os
import bcrypt
def register_user(connection, username, password):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        cursor.execute(query, (username, hashed_password))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:  # Now you can catch this
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def login_user(connection,username,password):
    try:
        cursor=connection.cursor()
        query="SELECT id,password_hash FROM users WHERE email=%s"
        values=(username,)
        cursor.execute(query,values)
        result=cursor.fetchone()
        user_ID,stored_password=result
        if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
        ):
            load_dotenv()
            token = jwt.encode(
                {"user_id": user_ID},
                os.getenv("SECRET_KEY"),
                algorithm="HS256"
            )
            return token
        else:
            return "Incorrect username or password"
        cursor.close()
    finally:
        if connection:
            connection.close()