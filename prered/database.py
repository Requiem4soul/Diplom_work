import mysql.connector
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

def save_parking_data_to_db(free_spots):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO parking_data (free_spots) VALUES (%s)"
            cursor.execute(insert_query, (free_spots,))
            connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            connection.close()

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_table(connection)
        connection.close()