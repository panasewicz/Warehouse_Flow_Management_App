import mysql.connector
from mysql.connector import Error
import datetime

def insert_to_database(values):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="***",
            database="products_scans"
        )
        cursor = connection.cursor()
        # Object DataTime converted to 2 objects Data and Time
        if isinstance(values["Data_And_Time"], str):
            dt = datetime.datetime.fromisoformat(values["Data_And_Time"])
            date_created = dt.date()
            time_created = dt.time()
        else:
            print(f"Value Data_And_Time is not of the correct format: {values['Data_And_Time']}")
            return
        # Check Empty string if yes we set "null" value
        error_comment = values["string"] if values["string"] else "null"
        # Call stored procedure
        cursor.callproc('InsertProduct', [values["int1"], values["int2"], values["int3"], values["int4"], error_comment, date_created, time_created])
        connection.commit()
        print("Values Insert to data Base.")
    except Error as e:
        print(f"Communication error with DataBase: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            
def fetch_data_from_database():
    #communication check
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Amar3",
            database="products_scans"
        )
        cursor = connection.cursor()
        query = "SELECT Order_Station_ID, Barcode_Number, to_write FROM write_value"
        cursor.execute(query)
        # Fetch rows from the database
        rows = cursor.fetchall()
        # Now 'rows' is a 2D list (or list of tuples) with the values of Barcode_Number and to_write columns
        # Make sure to close the cursor and connection to not consume resources
        cursor.close()
        connection.close()
        return rows
    except mysql.connector.Error as error:
        print("Failed to fetch data from MySQL table: {}".format(error))
# Fetch the data and store it in 'data'
data = fetch_data_from_database()
