from db_connection import create_connection
import mysql.connector

connection = None

try:
    connection = create_connection()

    if connection is None:
        print("Failed to connect to database.")

    else:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers")

        result = cursor.fetchone()

        print("Total customers:", result[0])

        cursor.close()

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed.")