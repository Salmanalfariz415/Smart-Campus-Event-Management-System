import mysql.connector
def submitl(connection,username,desc,org,st_date,end_date,st_time,end_time,venue,building,capacity,fee,reg,img,contact,website,tag):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO events (title, description, organizer, start_date, end_date, start_time, end_time, venue, building, capacity, fee, registration_required, image_url, contact_email, website, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values=(username,desc,org,st_date,end_date,st_time,end_time,venue,building,capacity,fee,reg,img,contact,website,tag,)
        cursor.execute(query,values)
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def eventcard(connection):
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM events ORDER BY id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            for key, value in row.items():
                if hasattr(value, '__str__') and not isinstance(value, (int, str, float, bool, type(None))):
                    row[key] = str(value)

        return rows
    except mysql.connector.Error as e:
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
