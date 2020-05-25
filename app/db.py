from mysql.connector import connect

def connectDB(host='localhost',database='testdb',user='root',password='national12',):
    return connect(host=host,database=database,user=user,password=password)