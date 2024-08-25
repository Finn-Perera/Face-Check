from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
import Boots_scrape2

load_dotenv()

connection = None
# host = os.getenv('DB_HOST')
# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASSWORD')
# database = os.getenv('DB_NAME')

def connector():
    return mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )

def checkBeforeCommit(connection):
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

def writeItemsToDB():
    try:
        connection = connector()

        if connection.is_connected():
            print("Connected to db")

            cursor = connection.cursor()
            items = Boots_scrape2.gather_items()
            if items == None:
                print("An error occured gathering items.")
                cursor.close()
                connection.close()
                return
            # name, price, stars, review_count, href, website
            sql_insert_query = """
            INSERT INTO items (item_name, price, rating, num_reviews, href, website)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            for item in items:
                cursor.execute(sql_insert_query, item)
            
            print("Changes have been made: ")
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            for item in rows:
                print(item)

            checkBeforeCommit(connection)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


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
            INSERT INTO items (item_name, price, rating, num_reviews, href, website)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = ("facewash", 5.10, 4.5, 10, "https://www.boots.com/the-ordinary-niacinamide-10-zinc-1-10267783", "Boots")
            cursor.execute(sql_insert_query, values)

            print("Changes have been made: ")
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            for item in rows:
                print(item)
            checkBeforeCommit(connection)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

def read():
    try:
        connection = connector()

        if connection.is_connected():
            print("Successfully connected to the databases")
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM items")
            for row in cursor.fetchall():
                print(row)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


#writeItem()

#read()

writeItemsToDB()