import jwt
from dotenv import load_dotenv
import os
import bcrypt
import datetime
import psycopg2

load_dotenv()

connection= psycopg2.connect(os.getenv("DATABASE_URL"))

def _make_token(user_id, user_type):
    """Return a signed JWT valid for 24 hours."""
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

def register_user(connection, username, password, user_type='user'):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (email, password_hash, user_type) VALUES (%s, %s, %s) RETURNING id"
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")
        cursor.execute(query, (username, hashed_password, user_type))
        user_id = cursor.fetchone()[0]
        connection.commit()
        token = _make_token(user_id, user_type)
        return {"user_id": user_id, "token": token}
    except psycopg2.Error as e:
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
        if result is None:
            return "Incorrect username or password"
        user_ID, stored_password, user_type = result
        # stored_password may be str or bytes depending on the column type
        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            return _make_token(user_ID, user_type)
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
        
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def register_organizer(connection, org_data):
    cursor = None
    try:
        cursor = connection.cursor()
        

        result = register_user(
            connection, 
            org_data['email'], 
            org_data['password'], 
            'organizer'
        )
        user_id = result['user_id']
        
        organizer_query = """
        INSERT INTO organizers 
        (user_id, org_name, org_type, org_description, contact_name, 
         contact_position, phone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
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
        organizer_id = cursor.fetchone()[0]
        connection.commit()
        
        return {
            'user_id': user_id,
            'organizer_id': organizer_id
        }
        
    except psycopg2.Error as e:
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()