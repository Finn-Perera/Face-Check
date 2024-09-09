from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
import Boots_scrape2
import The_Ordinary_scrape

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

def writeItemsToDB(items):
    try:
        connection = connector()

        if connection.is_connected():
            print("Connected to db")
            connection.start_transaction()
            cursor = connection.cursor()
            
            if items == None:
                print("No items passed in to write to DB")
                cursor.close()
                connection.close()
                return
            
            # name, price, stars, review_count, href, website, image_url

            insert_product_query = """
            INSERT INTO products (product_name, product_image)
            VALUES (%s, %s)
            """
            insert_option_query = """
            INSERT INTO product_options (product_id, price, rating, num_reviews, href, website)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            check_product_exists_query = """
            SELECT product_id FROM products WHERE product_name = %s
            """
            check_option_exists_query = """
            SELECT option_id FROM product_options WHERE product_id = %s AND href = %s
            """

            # Obsolete but maybe need to come back to them
            sql_insert_new_product_query = """
            INSERT INTO products (product_name, product_image)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
            product_image = VALUES(product_image);
            """
            sql_insert_new_option_query = """
            INSERT INTO product_options (product_id, price, rating, num_reviews, href, website)
            VALUES(%s, %s, %s, %s, %s, %s);
            ON DUPLICATE KEY UPDATE
                price = VALUES(price),
                rating = VALUES(rating),
                num_reviews = VALUES(num_reviews), 
                href = VALUES(href);
            """
            sql_select_product_query = """
            SELECT product_id
            FROM products 
            WHERE product_name = %s;
            """

            # Selects all changes
            sql_changes_made_select_query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.product_image,
                o.option_id,
                o.price,
                o.rating,
                o.num_reviews,
                o.href,
                o.website,
                o.last_updated
            FROM
                products p
            INNER JOIN
                product_options o ON p.product_id = o.product_id;
            """

            # Works, could probably be more efficient but this took hours to debug and may not be worth it.
            for item in items:
                name, price, stars, review_count, href, website, prod_img = item

                cursor.execute(check_product_exists_query, (name,))
                res = cursor.fetchone()

                if res:
                    prod_id = res[0]
                else:
                    cursor.execute(insert_product_query, (name, prod_img))
                    prod_id = cursor.lastrowid

                cursor.execute(check_option_exists_query, (prod_id, website))
                res = cursor.fetchone()

                if not res:
                    cursor.execute(insert_option_query, (prod_id, price, stars, review_count, href, website))
            
            print("Changes have been made: ")
            cursor.execute(sql_changes_made_select_query)
            rows = cursor.fetchall()
            for item in rows:
                print(item)

            checkBeforeCommit(connection)
    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
        #connection.rollback()
    finally:
        if connection and connection.is_connected():
            if cursor:
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
#writeItemsToDB(Boots_scrape2.gather_items())
writeItemsToDB(The_Ordinary_scrape.gather_items())