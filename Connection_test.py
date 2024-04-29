import mysql.connector

connection = mysql.connector.connect(
    user='root',
    database='c2c_project',
    password='2gd4fart'
)

cursor = connection.cursor()
testQuery = ("SELECT * FROM c2c_project")
cursor.execute(testQuery)

for row in cursor:
    print(row)



cursor.close()
connection.close()
