# File to establish the database connection
import pymysql as sql

def db_connect(db):
    # function to connect to the database and return the connection and cursor objects
    conn = sql.connect(host='localhost', user='root', password='', database=db)
    cursor = conn.cursor()
    return conn, cursor

def db_close(conn):
    # function to close the database connection and cursor
    conn.close()
    
