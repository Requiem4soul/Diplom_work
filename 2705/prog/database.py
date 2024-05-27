import mysql.connector
import cv2
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Замените на ваше имя пользователя
            password='',  # Замените на ваш пароль, если есть
            database='parking_system'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def save_image_to_db(frame):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Удаляем предыдущее изображение
            cursor.execute("DELETE FROM last_updated_image")

            # Преобразуем кадр в бинарные данные и сохраняем их в базе данных
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
            clear_old_parking_data(connection, max_records)  # Удаление старых записей
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            connection.close()

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_table(connection)
        connection.close()