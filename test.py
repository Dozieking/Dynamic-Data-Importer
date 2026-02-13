import pymysql as sql
conn = sql.connect(host='localhost', user='root', password='', database='test_db')
cursor = conn.cursor()

# # 1️⃣ Create Database
# cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")

# # Use the database
# cursor.execute("USE test_db")

# # 2️⃣ Create Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100),
#     age INT
# )
# """)

# # 3️⃣ Insert Data
# sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
# values = [
#     ("Alice", 25),
#     ("Bob", 30),
#     ("Charlie", 22)
# ]

# cursor.executemany(sql, values)

# # Commit changes
# conn.commit()

# print("Database, table, and data created successfully!")
cursor.execute(f"SHOW COLUMNS FROM `{'users'}`")
cols_info = cursor.fetchall()
print(cols_info)

# Close connection
cursor.close()
conn.close()


