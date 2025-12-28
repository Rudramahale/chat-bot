import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1436",
    database="online_shop",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()
# cursor.execute("SELECT * FROM orders")
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

def get_id(id):
    cursor.execute("select * from orders where order_id = %s",(id,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

def get_details(id):
    cursor.execute("select * from orders where order_id = %s",(id,))
    result = cursor.fetchall()
    if result:
        return result
    else:
        return None

