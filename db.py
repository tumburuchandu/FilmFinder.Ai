import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    database="movie_app"
)

cursor = db.cursor()