import mysql.connector
import cv2
from mysql.connector import Error
import numpy as np


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='parking_system'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def save_parking_data(car_spots, check_spots, ip_address):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            car_spots_str = ",".join(map(str, [item for sublist in car_spots for item in sublist]))
            check_spots_str = ",".join(map(str, [item for sublist in check_spots for item in sublist]))

            check_query = "SELECT COUNT(*) FROM parking_data WHERE ip_address = %s"
            cursor.execute(check_query, (ip_address,))
            result = cursor.fetchone()[0]

            if result > 0:
                update_query = """
                    UPDATE parking_data 
                    SET car_spots = %s, check_spots = %s, timestamp = CURRENT_TIMESTAMP 
                    WHERE ip_address = %s
                """
                cursor.execute(update_query, (car_spots_str, check_spots_str, ip_address))
            else:
                insert_query = """
                    INSERT INTO parking_data (car_spots, check_spots, ip_address, timestamp) 
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """
                cursor.execute(insert_query, (car_spots_str, check_spots_str, ip_address))

            connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            connection.close()

def save_update_to_db(frame, free_spots, ip_address):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='parking_system'
        )

        cursor = connection.cursor()

        ret, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()

        check_query = "SELECT COUNT(*) FROM parking_updates WHERE ip_address = %s"
        cursor.execute(check_query, (ip_address,))
        result = cursor.fetchone()[0]

        if result > 0:
            update_query = """
                UPDATE parking_updates
                SET image_data = %s, free_spots = %s, timestamp = CURRENT_TIMESTAMP
                WHERE ip_address = %s
            """
            cursor.execute(update_query, (image_data, free_spots, ip_address))
        else:
            insert_query = """
                INSERT INTO parking_updates (image_data, free_spots, ip_address)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (image_data, free_spots, ip_address))

        connection.commit()
        print("Data saved successfully!")

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def save_image_to_db(frame):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("DELETE FROM last_updated_image")

            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                binary_data = buffer.tobytes()
                cursor.execute("INSERT INTO last_updated_image (image_data) VALUES (%s)", (binary_data,))
                connection.commit()
                print("Image saved to database successfully")
            else:
                print("Error: Couldn't encode the frame to JPEG format")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()

def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS parking_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        free_spots INT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"Error: '{e}'")


def clear_old_parking_data(connection, max_records):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM parking_data")
        count = cursor.fetchone()[0]

        if count > max_records:
            excess_records = count - max_records
            cursor.execute(f"DELETE FROM parking_data ORDER BY timestamp LIMIT {excess_records}")
            connection.commit()
            print(f"{excess_records} old parking data records cleared successfully")
        else:
            print("No excess records to clear")
    except Error as e:
        print(f"Error: '{e}'")

def save_parking_data_to_db(free_spots, max_records=100):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO parking_data (free_spots) VALUES (%s)"
            cursor.execute(insert_query, (free_spots,))
            connection.commit()
            print("Data inserted successfully")
            clear_old_parking_data(connection, max_records)
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            connection.close()

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_table(connection)
        connection.close()