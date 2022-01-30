import MySQLdb


# 订单查询
# 传入需要查找的属性和属性值字符串，空串代表不设限制，结果按照order_by参数排序
def order_query(attribute_type, attribute_value, status='', order_by='order_no'):
    # attributes = ['order_no', 'ID', 'Room_ID', 'price', 'discount', 'num_customers', 'Dealer_ID', 'date', 'time']
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from order_list "
    if attribute_type != '':
        sql += "where %s= '%s' " % (attribute_type, attribute_value)
    if status != '':
        sql += "and order_status= '%s'" % status
    sql += " order by %s;" % order_by

    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results


def check_in_query(attribute_type, attribute_value, order_by='order_no'):
    # attributes = ['order_no', 'ID', 'Room_ID', 'price', 'discount', 'num_customers', 'Dealer_ID', 'date', 'time']
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from check_in  "
    if attribute_type != '':
        sql += "where %s= '%s' " % (attribute_type, attribute_value)

    sql = sql + "order by " + order_by + ";"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results
