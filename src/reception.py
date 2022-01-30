import time
import datetime
import MySQLdb
import order_manage


# 预订功能
# 传入客户选定的房间号Room_ID
def make_order(order_no, ID, Room_ID, num_customers, Dealer_ID, start_date, end_date, order_date, cur_time,order_type='个人'):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # find price
    sql = "select price from room where room_id='%s';" % Room_ID
    cursor.execute(sql)
    results = cursor.fetchall()
    # for row in results:
    price = results[0][0]

    # find discount
    sql = "select discount from VIP where id= '%s';" % ID
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results)==0:
        discount=1
    else:
        discount = results[0][0]
    # insert
    sql = "insert into order_list values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '预订中','%s');" % \
            (order_no, ID, Room_ID, price, discount, num_customers, Dealer_ID, start_date, end_date, order_date, cur_time, order_type)

    cursor.execute(sql)
    db.close()


# 团队预订
# 传入房间号、客户数的数组
def group_make_order(order_no, ID, Room_ID, num_customers, Dealer_ID, start_date, end_date, order_date, cur_time):
    for i in range(0, len(Room_ID)):
        make_order(order_no[i], ID, Room_ID[i], num_customers, Dealer_ID, start_date, end_date, order_date, cur_time,'团体')


# 登记功能
# 一次登记一个房间的客户
def check_in(order_no, ID, customer_name, phone, cur_date, cur_time):  # 登记
    result = order_manage.order_query("order_no", order_no, '预订中')
    Room_ID = result[0][2]
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306,autocommit=True)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for i in range(0, len(ID)):
        sql = "insert into check_in values('%s','%s','%s','%s','%s','%s','%s');" % \
                (order_no, Room_ID, ID[i], customer_name[i], phone[i], cur_date, cur_time)
        cursor.execute(sql)
    sql = "update order_list set order_status='入住中' where order_no='%s';" % order_no
    cursor.execute(sql)
    db.close()


# 团体登记
# 传入团体数据的二维数组
def group_check_in(leader_ID, customer_name, phone, cur_date, cur_time):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306,autocommit=True)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    results = order_manage.order_query("id", leader_ID, status='预订中')
    for i in range(0, len(results)):
        order_no = results[i][0]
        room_ID = results[i][2]

        sql = "insert into check_in values('%s','%s','%s','%s','%s','%s','%s');" % \
                (order_no, room_ID, leader_ID, customer_name, phone , cur_date, cur_time)
        cursor.execute(sql)

        sql = "update order_list set order_status='入住中' where order_no='%s';" % order_no
        cursor.execute(sql)

    db.close()


# 房间号 checkout
def check_out(Room_ID):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306,autocommit=True)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    results = order_manage.order_query('room_id', Room_ID, '入住中')
    order_no = results[0][0]
    id = results[0][1]
    price = results[0][3]
    discount = results[0][4]
    start_date = results[0][7]
    end_date = results[0][8]
    sql = "set SQL_SAFE_UPDATES = 0;"
    cursor.execute(sql)
    sql = "delete from check_in where order_no='%s';" % order_no
    cursor.execute(sql)
    sql = "update order_list set order_status='已完成' where order_no='%s' and order_status='入住中';" % order_no
    cursor.execute(sql)
    sql = "set SQL_SAFE_UPDATES = 1;"
    cursor.execute(sql)
    db.close()
    date1 = time.strptime(start_date, "%Y%m%d")
    date2 = time.strptime(end_date, "%Y%m%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    day = str(date2 - date1)
    days = int(day.replace(' days, 0:00:00', ''))
    total = days * float(price) * float(discount)
    return total, id


# 预订人ID checkout
def group_check_out(ID):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306,autocommit=True)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    results = order_manage.order_query('id', ID, '入住中')
    sql = "set SQL_SAFE_UPDATES = 0;"
    cursor.execute(sql)
    total = 0
    for row in results:
        order_no = row[0]
        price = row[3]
        discount = row[4]
        start_date = row[7]
        end_date = row[8]
        sql = "delete from check_in where order_no='%s';" % order_no
        cursor.execute(sql)
        sql = "update order_list set order_status='已完成' where order_no='%s';" % order_no
        cursor.execute(sql)
        date1 = time.strptime(start_date, "%Y%m%d")
        date2 = time.strptime(end_date, "%Y%m%d")
        date1 = datetime.datetime(date1[0], date1[1], date1[2])
        date2 = datetime.datetime(date2[0], date2[1], date2[2])
        day = str(date2 - date1)
        days = int(day.replace(' days, 0:00:00', ''))
        total += days * float(price) * float(discount)
    sql = "set SQL_SAFE_UPDATES = 1;"
    cursor.execute(sql)
    db.close()
    return total
