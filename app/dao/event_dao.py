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


