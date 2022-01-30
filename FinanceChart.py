'''
财务管理模块
1.财务报表
'''
import MySQLdb
import datetime
import calendar

def Query_Room_Num(): #查询room表中房间的数量，计算空置率用
    query = 'select * from room'
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    return len(res)


def Query_Room_Num_RoomType(room_type:str): #查询room表中指定type的房间的数量，计算空置率用
    query = 'select * from room where room_type = \'' + room_type + '\' ;'
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    return len(res)


def FinanceChart_Sum_CertainMonth(year:int, month:int):
    """
    【不指定房间类型】输入年份和月份，查询指定月份的收入总数（order_list中已完成的）
    """
    d1 = datetime.date(year, month, 1)
    d2 = datetime.date(year, month, calendar.monthrange(year, month)[1])
    d1 = d1.strftime("%Y%m%d")
    d2 = d2.strftime("%Y%m%d")
    query = 'select price,start_date,end_date,room_id \
                from order_list where order_status = \'已完成\' and \
                start_date >= \'' + d1 + \
                '\' and start_date <= \'' + d2 + '\';'

    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    sum = 0
    for t in res:
        if t[2] > d2:
            sum += (int(d2)-int(t[1]))*t[0]
        else:
            sum += (int(t[2])-int(t[1])+1)*t[0]

    return sum, len(res)/Query_Room_Num()

def FinanceChart_Sum_CertainMonth_RoomType(year:int, month:int, room_type:str):
    """
    【指定房间类型】输入年份和月份，查询指定月份的收入总数（order_list中已完成的）
    """
    d1 = datetime.date(year, month, 1)
    d2 = datetime.date(year, month, calendar.monthrange(year, month)[1])
    d1 = d1.strftime("%Y%m%d")
    d2 = d2.strftime("%Y%m%d")
    query = 'select price,start_date,end_date,room_id \
                from order_list where order_status = \'已完成\' and \
                start_date >= \'' + d1 + \
                '\' and start_date <= \'' + d2 + '\';'
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    sum = 0
    for t in res:
        room_id = t[3]
        query = 'select room_type from room where room_id = \'' + room_id + '\';'
        cursor = db.cursor()
        cursor.execute(query)
        tmp = cursor.fetchall()
        if tmp[0][0] == room_type:
            if t[2] > d2:
                sum += (int(d2)-int(t[1]))*t[0]
            else:
                sum += (int(t[2])-int(t[1])+1)*t[0]

    db.close()
    return sum, len(res)/Query_Room_Num_RoomType(room_type)

def FinanceChart_Sum_CertainMonth_Pie_with_type(year:int, month:int):
    sum = []
    tt = ['舒适单人房','舒适双人房','豪华单人房','豪华双人房','行政套房']
    for t in tt:
        sum.append(FinanceChart_Sum_CertainMonth_RoomType(year,month,t))


    s = str(year) + '.' + str(month) + '单月财务报表'
    s_html = s + '.html'

    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = (
        Pie()
        .add("", [list(z) for z in zip(tt, sum)])
        .set_colors(["blue", "green", "red", "pink", "orange"])
        .set_global_opts(title_opts=opts.TitleOpts(title=s))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render(s_html)
    )
    return


def FinanceChart_Sum_All():
    """
    【不指定房间类型】查询过去所有记录的月份的收入总数
    """
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    query = 'select min(start_date) from (select start_date from order_list where order_status=\'已完成\') as a;'
    cursor.execute(query)
    min = cursor.fetchall()
    query = 'select max(end_date) from (select end_date from order_list where order_status=\'已完成\') as a;'
    cursor.execute(query)
    max = cursor.fetchall()
    db.close()
    min = min[0][0]
    max = max[0][0]

    year_begin = int(min[0:4])
    year_end = int(max[0:4])
    month_begin = int(min[4:6])
    month_end = int(max[4:6])

    month_list = []
    sum_list = []
    for year in range(year_begin, year_end+1):
        if year == year_begin:
            for month in range(month_begin, 13):
                month_list.append(str(year)+'.'+str(month))
                sum_list.append(FinanceChart_Sum_CertainMonth(year,month))
        elif year == year_end:
            for month in range(1, month_end):
                month_list.append(str(year)+'.'+str(month))
                sum_list.append(FinanceChart_Sum_CertainMonth(year,month))
        else:
            for month in range(1,13):
                month_list.append(str(year)+'.'+str(month))
                sum_list.append(FinanceChart_Sum_CertainMonth(year,month))

    return month_list, sum_list


