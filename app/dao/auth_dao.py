import mysql.connector
import jwt
from dotenv import load_dotenv
import os
import bcrypt
def register_user(connection, username, password, user_type='user'):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (email, password_hash, user_type) VALUES (%s, %s, %s)"
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        cursor.execute(query, (username, hashed_password, user_type))
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
        query="SELECT id,password_hash,user_type FROM users WHERE email=%s"
        values=(username,)
        cursor.execute(query,values)
        result=cursor.fetchone()
        user_ID,stored_password,user_type=result
        if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
        ):
            load_dotenv()
            token = jwt.encode(
                {"user_id": user_ID, "user_type": user_type},
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

def get_user_details(connection, user_id):
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Get basic user info
        user_query = "SELECT id, email, user_type FROM users WHERE id = %s"
        cursor.execute(user_query, (user_id,))
        user_result = cursor.fetchone()
        
        if not user_result:
            return None
            
        user_data = {
            'id': user_result[0],
            'email': user_result[1], 
            'user_type': user_result[2]
        }
        
        # If organizer, get organizer details
        if user_result[2] == 'organizer':
            org_query = """
            SELECT id, org_name, org_type, org_description, 
                   contact_name, contact_position, phone 
            FROM organizers WHERE user_id = %s
            """
            cursor.execute(org_query, (user_id,))
            org_result = cursor.fetchone()
            
            if org_result:
                user_data['organizer_info'] = {
                    'id': org_result[0],
                    'org_name': org_result[1],
                    'org_type': org_result[2],
                    'org_description': org_result[3],
                    'contact_name': org_result[4],
                    'contact_position': org_result[5],
                    'phone': org_result[6]
                }
        
        return user_data
        
    except mysql.connector.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def register_organizer(connection, org_data):
    cursor = None
    try:
        cursor = connection.cursor()
        
        user_id = register_user(
            connection, 
            org_data['email'], 
            org_data['password'], 
            'organizer'
        )
        
        
        organizer_query = """
        INSERT INTO organizers 
        (user_id, org_name, org_type, org_description, contact_name, 
         contact_position, phone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        organizer_values = (
            user_id,
            org_data['org_name'],
            org_data['org_type'], 
            org_data.get('org_description', ''),
            org_data['contact_name'],
            org_data['contact_position'],
            org_data['phone']
        )
        
        cursor.execute(organizer_query, organizer_values)
        connection.commit()
        
        return {
            'user_id': user_id,
            'organizer_id': cursor.lastrowid
        }
        
    except mysql.connector.Error as e:
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()