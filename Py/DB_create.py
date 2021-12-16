import mysql.connector
from mysql.connector import errorcode
from mysql.connector.constants import SQLMode

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456ab"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE EGTB")

#create database for storing EGTB
try:
    mycursor.execute("CREATE DATABASE EGTB")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_DB_CREATE_EXISTS:
        print("DB already exists.")
    else:
        print(err.msg)
else:
    print("OK")

