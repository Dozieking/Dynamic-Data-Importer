# Sample SQL script to create a database and a table, and insert some sample data. This can be used for testing purposes with the dynamic importer.
from importer.database import db_connect, db_close
import pymysql as sql


username = input("Enter the database username: ")
password = input("Enter the database password: ")

conn = sql.connect(host='localhost', user=username, password=password)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS dynamic_importer_test")
print("Database 'dynamic_importer_test' created successfully (if it did not already exist).")
cursor.execute("USE dynamic_importer_test")


cursor.execute("""
    
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
)


insert_query = """
INSERT INTO users (name, email, age)
VALUES (%s, %s, %s)
"""

values = ("John Doe", "john@example.com", 25)

cursor.execute(insert_query, values)
conn.commit()
print("Sample data inserted into 'users' table successfully.")
