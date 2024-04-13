import mysql.connector

conn = mysql.connector.connect(
    user='username', password='password', host="127.0.0.1", port="3306", database="WaterCarrier"
)

cursor = conn.cursor()

with open('init.sql', 'r') as f:
    for line in f:
        cursor.execute(line)

conn.commit()
cursor.close()
conn.close()