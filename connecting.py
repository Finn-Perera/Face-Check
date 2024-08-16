from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os

load_dotenv()


connection = None
# host = os.getenv('DB_HOST')
# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASSWORD')
# database = os.getenv('DB_NAME')
def writeItem():
    try:
        connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )

        if connection.is_connected():
            print("Successfully connected to the databases")

            cursor = connection.cursor()
            sql_insert_query = """
            INSERT INTO item (ItemName, Rating, NumReviews, href, website)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = ("facewash", 4.5, 10, "https://www.boots.com/the-ordinary-niacinamide-10-zinc-1-10267783", "Boots")
            cursor.execute(sql_insert_query, values)

            print("Changes have been made: ")
            cursor.execute("SELECT * FROM item")
            rows = cursor.fetchall()
            for item in rows:
                print(item)

            user_input = input("Type 'commit' to save changes to the database or 'rollback' to discard: ").strip().lower()

            if user_input == 'commit':
                connection.commit()
                print("Record inserted successfully")
                print("Transaction Committed.")
            elif user_input == 'rollback':
                connection.rollback()
                print("Transaction rolled back.")
            else:
                print("Invalid input, rolling back transaction.")
                connection.rollback()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

def read():
    try:
        connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )

        if connection.is_connected():
            print("Successfully connected to the databases")
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM item")
            for row in cursor.fetchall():
                print(row)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


writeItem()

read()