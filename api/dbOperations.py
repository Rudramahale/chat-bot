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

def update_refund_status(id):
    try:
        cursor.execute("update orders set order_status = 'CANCELLED' where order_id = %s",(id,))
        cursor.execute("update orders set payment_status = 'REFUND_INITIATED' where order_id = %s",(id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating refund status: {e}")
        return False

cursor.execute("update orders set order_status = 'SHIPPED' where order_id = 2")
cursor.execute("update orders set payment_status = 'NONE' where order_id = 2")
conn.commit()

