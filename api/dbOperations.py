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
        return result
    else:
        return None

def get_status(id):
    cursor.execute("select order_status from orders where order_id = %s",(id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None

