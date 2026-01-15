import mysql.connector
def register_user(connection, username, password):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:  # Now you can catch this
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()