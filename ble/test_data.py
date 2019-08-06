import mysql.connector

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'ble'

myConnection = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)

myCursor = myConnection.cursor()
myCursor.execute("SELECT temp_1, temp_2, temp_3, temp_4, pressure_1, pressure_2, pressure_3, pressure_4 from data  ORDER BY ID DESC LIMIT 1")
myresult = myCursor.fetchall()
print myresult
#print str(myresult[0][0])

"""try:
    with myConnection.cursor() as cursor:
        sql = "SELECT temp_1, temp_2 from data  ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    myConnection.close()"""