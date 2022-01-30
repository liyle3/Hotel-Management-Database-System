"""
客房管理模块
1.客房状态查询
    ROOM_PRICE()
2.修改客房价格
    show_room_status_1()
    show_room_status_2()
"""
import MySQLdb
import datetime


def ROOM_PRICE(newprice:str, room_id:str):
    '''
    1.newprice修改之后的价格
    2.room_id房间号
    '''
    query = 'update room set price = ' + newprice + ' where room_id = \'' + room_id + '\';'
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.commit()
    db.close()
    return res


def GET_PRICE(RID):
    """
    查询房间价格
    """
    query = "select price from room where room_id = '%s';" % RID
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    price = res[0][0]
    return price



def ROOM_STATUS(date:datetime.date, room_id:str, order_status:str, room_type:str, db):
    """
    指定具体日期、房间、状态、类型，若存在，则返回元组，否则返回None
    1.date查询日期 datetime.date()类型，如 data = datetime.date(1956,1,1)\n
    2.room_id查询 某个房间如'230'\n
    3.order_status查询 '空置' 或'入住中' 或'预订中' 或'已完成'\n
    4.room_type查询'舒适单人房','舒适双人房','豪华单人房','豪华双人房','行政套房'\n
    返回元组的结构为 (1日期datetime.date 2房间号 3状态 4类型 5现在价格 )
    """
    query = 'select price from room where room_id = \'' + room_id +'\' and room_type= \'' + room_type + '\';'
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    # db.close()
    if len(res) == 0:
        return None
    else:
        price = res[0][0]


    if order_status == '空置': #空置的不会出现在order_list表格上
        query = 'select room.room_id, order_status, room_type,room.price \
            from room join order_list on room.room_id = order_list.room_id'
        query = query + ' where room.room_id = \'' + room_id + '\''
        query = query + ' and start_date <= \'' + date.strftime("%Y%m%d") + '\''
        query = query + ' and end_date >= \'' + date.strftime("%Y%m%d") + '\''
        query = query + ' and room.room_type = \'' + room_type + '\';'

        cursor = db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 1:
            return None
        else:
            r = (date, room_id, order_status, room_type, price)
            return r
    else:
        query = 'select room.room_id,order_status,room_type,room.price \
            from room join order_list on room.room_id = order_list.room_id'
        query = query + ' where room.room_id = \'' + room_id + '\''
        query = query + ' and start_date <= \'' + date.strftime("%Y%m%d") + '\''
        query = query + ' and end_date >= \'' + date.strftime("%Y%m%d") + '\''
        query = query + ' and order_status = \'' + order_status + '\''
        query = query + ' and room.room_type = \'' + room_type + '\';'
        cursor = db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()

        if len(res) == 1:
            r = (date,) + res[0]
            return r
        else:
            return None


def show_room_status_1(startYear:int, startMonth:int, startDay:int, endYear:int, endMonth:int, endDay:int, room_id:str, order_status:str, room_type:str):
    """
    指定日期、房间、状态、类型，若存在，则返回元组的元组，否则返回空元组\n
    注意这个函数与show_room_status_2的区别:这个函数会返回起止日期的每一天中所有满足条件的房间+日期，而不要求该房间在整个起止日期区间都满足条件\n
    输入格式如下:\n
    1.头六个日期信息\n
    2.room_id 查询 某个房间如'230' 或全部'all'\n
    3.order_status查询 '空置' 或'入住中' 或'预定中' 或'已完成' 或'all'\n
    4.room_type查询'舒适单人房','舒适双人房','豪华单人房','豪华双人房','行政套房'或all\n
    返回元组的结构为 (1日期 2房间号 3状态 4类型 5订单时价格 6现在价格)
    """
    date = []
    date.append(datetime.date(startYear,startMonth,startDay))
    date.append(datetime.date(endYear,endMonth,endDay))

    room_list = []
    if room_id != 'all':
        room_list.append(room_id)
    else:
        query = 'select room_id from room;'
        db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
        cursor = db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        db.close()
        for i in res:
            room_list.append(i[0])
    state_list = []
    if order_status == 'all':
        state_list.append('空置')
        state_list.append('入住中')
        state_list.append('预订中')
        state_list.append('已完成')
    else:
        state_list.append(order_status)
    type_list = []
    if room_type == 'all' :
        type_list.append('舒适单人房')
        type_list.append('舒适双人房')
        type_list.append('豪华单人房')
        type_list.append('豪华双人房')
        type_list.append('行政套房')
    else:
        type_list.append(room_type)
    date_list = []
    date_begin = date[0]
    date_end = date[1]
    tmp = date_begin
    delta = datetime.timedelta(days=1)
    day = 0
    while tmp <= date_end:
        date_list.append(tmp)
        tmp += delta
        day += 1

    res = ()
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    for i in date_list:
        for j in room_list:
            for u in state_list:
                for v in type_list:
                    one = ROOM_STATUS(i,j,u,v,db)
                    if one != None:
                        res = res + (one,)
    db.close()
    return res


def show_room_status_2(startYear:int, startMonth:int, startDay:int, endYear:int, endMonth:int, endDay:int, room_type:str):
    """
    输入:\n
    1.开始的年\n
    2.开始的月\n
    3.开始的日\n
    4.结束的年\n
    5.结束的月\n
    6.结束的日\n
    7.房间类型,可以为'舒适单人房','舒适双人房','豪华单人房','豪华双人房','行政套房','all'\n
    返回满足要求的空置房间以及对应价格（返回两个元组，第一个是房间号，第二个是价格）
    """
    room_list = []
    query = 'select room_id from room;'
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    for i in res:
        room_list.append(i[0])
    type_list = []
    if room_type == 'all' :
        type_list.append('舒适单人房')
        type_list.append('舒适双人房')
        type_list.append('豪华单人房')
        type_list.append('豪华双人房')
        type_list.append('行政套房')
    else:
        type_list.append(room_type)
    date_list = []
    date_begin = datetime.date(startYear,startMonth,startDay)
    date_end = datetime.date(endYear,endMonth,endDay)
    tmp = date_begin
    delta = datetime.timedelta(days=1)
    day = 0
    while tmp <= date_end:
        date_list.append(tmp)
        tmp += delta
        day += 1
    res = ()
    res_price = ()
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    for j in room_list:
        spare_day = 0
        for i in date_list:
            for v in type_list:
                one = ROOM_STATUS(i,j,'空置',v,db)
                if one != None:
                    spare_day += 1
                    tmp_price = one[4]
        if spare_day == day:
            res = res + (j,)
            res_price = res_price + (tmp_price,)
    db.close()
    return res, res_price




