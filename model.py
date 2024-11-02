import mysql.connector
import setting

def create_database_if_not_exists():
    # Connect without specifying the database
    connection = mysql.connector.connect(
        host=setting.SERVER_HOST,
        user=setting.SERVER_USER,
        password=setting.SERVER_PASSWORD
    )

    cursor = connection.cursor()
    
    # Check if database exists; if not, create it
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {setting.SERVER_DATABASE}")
        print(f"Database '{setting.SERVER_DATABASE}' checked/created successfully.")
    except mysql.connector.Error as error:
        print(f"Failed to create database: {error}")
    finally:
        cursor.close()
        connection.close()

create_database_if_not_exists()

# Now, connect to the specified database
connection = mysql.connector.connect(
    host=setting.SERVER_HOST,
    user=setting.SERVER_USER,
    password=setting.SERVER_PASSWORD,
    database=setting.SERVER_DATABASE
)

class Model:
    def __init__(self, name, sql):
        self.name = name
        self.migrate(sql)

    def migrate(self, sql):
        try:
            print(f"Connected to MySQL Server version {connection.server_version}")
            
            cursor = connection.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.name} (id INT AUTO_INCREMENT PRIMARY KEY)")
            print(f"Table '{self.name}' created successfully.")
            
            connection.commit()
        except mysql.connector.Error as error:
            print("Failed to connect to MySQL Server:", error)
        finally:
            cursor.close()
            connection.close()
