from RoomManage import *
from FinanceChart import *
from reception import *
from order_manage import *
from employee import *
from VIP import *
import time
import getpass

ORDER_NO = 1
Dealer_ID = "00000000"
ADMIN_PASSWORD = "0x123456"
USER_PASSWORD = "0x654321"


def Reservation():
    global ORDER_NO
    # Label:
    while True:
        prices = [188, 288, 388, 488, 588]
        num_customers = [1, 1, 2, 2, 2]

        print("------------------------------------------------")
        print("                 订房界面                        ")
        print("1--个人订房\t 2--团体订房\t 0--退出当前页面\n")
        team = input("请选择操作：")
        if team == "0":
            return

        print("\n可选房间类型：")
        print("1--舒适单人房      2--豪华单人房")
        print("3--舒适双人房      4--豪华双人房")
        print("5--行政套房")
        type = input("请选择房间类型：")
        ID = input("请输入身份证号码(18位):")
        people = input("请选择入住人数：")
        start = input("请输入入住日期(2022/1/1)：")
        end = input("请输入退房日期(2022/1/1)：")
        num = 1
        start_list = start.split('/')
        if len(start_list[1]) == 1:
            start_list[1] = '0' + start_list[1]

        if len(start_list[2]) == 1:
            start_list[2] = '0' + start_list[2]

        end_list = end.split('/')
        if len(end_list[1]) == 1:
            end_list[1] = '0' + end_list[1]

        if len(end_list[2]) == 1:
            end_list[2] = '0' + end_list[2]

        start = start_list[0] + start_list[1] + start_list[2]
        end = end_list[0] + end_list[1] + end_list[2]

        #当前时间
        cur_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        time_list = cur_time.split(' ')
        curdate = time_list[0]
        curtime = time_list[1]

        if team == "2":
            num = input("请输入订房数量：")

        num = int(num)
        if type == 0:
            return 0
        type = int(type)
        room_types = ["舒适单人房", "豪华单人房", "舒适双人房", "豪华双人房", "行政套房"]
        #客房状态查询
        Available, Available_price = show_room_status_2(int(start_list[0]), int(start_list[1]), int(start_list[2]), int(end_list[0]), int(end_list[1]), int(end_list[2]), room_types[type-1])

        if len(Available) == 0:
            print("房间已满，请选择其他房间类型")
            continue
        elif len(Available) < num:
            print("房源不足！")
            continue
        else:
            if team == "2":
                print("已为您自动分配房间, 是否确定下单：")
                operation = input("0--取消 \t 1--确定\n")
                if operation == "1":
                    no_list = []
                    room_id = []

                    for k in range(num):
                        cur_no = str(ORDER_NO)
                        len_no = len(cur_no)
                        for kobe in range(10-len_no):
                            cur_no = '0' + cur_no

                        ORDER_NO += 1
                        no_list.append(cur_no)
                        room_id.append(Available[k])

                    print(room_id)
                    group_make_order(no_list, ID, room_id, num, Dealer_ID, start, end, curdate, curtime)
                    print("订房成功！")
                    continue

            else:
                print("共有%d个房间可供选择："%(len(Available)))

                print("房间号\t价格")
                for Room_ID in Available:
                    print("%s\t%d"%(Room_ID, prices[type-1]))

                RID = "000"
                while RID not in Available:
                    RID = input("请选择房间号：")
                    if RID in Available:
                        break

                print("当前选择房间号为%s, 是否确定下单："%(RID))
                operation = input("0--取消 \t 1--确定\n")
                if operation == "1":
                    cur_no = str(ORDER_NO)
                    len_no = len(cur_no)
                    for kobe in range(10-len_no):
                        cur_no = '0' + cur_no
                        ORDER_NO += 1

                    make_order(cur_no, ID, RID, num, Dealer_ID, start, end, curdate, curtime)
                    print("订房成功！")
                    if curdate == start:
                        check_in()
                        continue

    return 1


def CHECK_IN():
    #当前时间
    cur_time = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
    time_list = cur_time.split(' ')
    curdate = time_list[0]
    curtime = time_list[1]
    print("------------------------------------------------")
    print("               登记入住界面                      ")
    team = input("请选择类型： 0--个人登记\t 1--团体登记 \n")
    if team == "1":
        print("请输入领队的相关信息：")
        ID = input("身份证号：")#当前时间
        result = order_query("id", ID)
        order_no = result[0][0]
        num = result[0][5]
        start = result[0][7]
        if curdate != start:
            print("入住日期有误！")
            return


        name = input("名字：")
        phone = input("联系电话：")

        group_check_in(ID, name, phone, curdate, curtime)

    #个人登记
    else:
        ID = input("请输入登记的身份证号：")#当前时间
        result = order_query("id", ID)
        order_no = result[0][0]
        num = result[0][5]
        start = result[0][7]
        if curdate != start:
            print("入住日期有误！")
            return

        ID = []
        name = []
        phone = []

        if num > 1:
            print("请输入入住人员的相关信息：")
            ID1 = input("旅客1身份证号：")#当前时间
            name1 = input("旅客1名字：")
            phone1 = input("旅客1联系电话：")
            ID2 = input("旅客2身份证号：")#当前时间
            name2 = input("旅客2名字：")
            phone2 = input("旅客2联系电话：")
            ID.append(ID1)
            ID.append(ID2)
            name.append(name1)
            name.append(name2)
            phone.append(phone1)
            phone.append(phone2)

        else:
            print("请输入入住人员的相关信息：")
            ID1 = input("旅客身份证号：")#当前时间
            name1 = input("旅客名字：")
            phone1 = input("旅客联系电话：")
            ID.append(ID1)
            name.append(name1)
            phone.append(phone1)

        check_in(order_no, ID, name, phone, curdate, curtime)


def CHECK_OUT():
    cur_time = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
    time_list = cur_time.split(' ')
    curdate = time_list[0]
    curtime = time_list[1]
    print("------------------------------------------------")
    print("               退房结账界面                      ")
    team = input("请选择类型： 0--个人退房\t 1--团体退房\n")

    if team == "1":
        ID = input("请输入领队身份证号码：")
        money = group_check_out(ID)
        print("应付金额/元：%f" %(money))
        print("退房成功！")
        VIP_POINT(ID, money)

    else:
        RID = input("请输入房间号：")
        money, id = check_out(RID)
        print("应付金额/元：%f" %(money))
        print("退房成功！")
        VIP_POINT(id, money)


def UPDATE_PRICE():
    while True:
        print("------------------------------------------------")
        print("               定价修改界面                      ")
        RID = input("请输入房间号：")
        old_price = GET_PRICE(RID)
        print("房间" + RID + "当前定价为" + str(old_price))
        price = input("请输入修改后的价格：")
        ROOM_PRICE(price, RID)
        print("修改成功！")
        op = input("请选择操作：0--退出当前界面\t 1--继续修改\n")
        if op == "0":
            return



def FINANCE():
    while True:
        print("------------------------------------------------")
        print("               财务报表查询界面                   ")
        print("请选择查询类型：")
        type = input("1--ALL\t 2--年份-月份 \t 3--年份-月份-房间类型\t 0--退出当前界面\n")

        if type == "0":
            return

        elif type == "1":
            print("月份\t收入\t\t入住率")
            months, sums = FinanceChart_Sum_All()

            for month, sum in zip(months, sums):
                print(str(month) + "\t" + str(sum[0]) + "\t" + str(sum[1]) + "%")

        elif type == "2":
            year = input("请输入年份：")
            month = input("请输入月份：")
            num, rate = FinanceChart_Sum_CertainMonth(int(year), int(month))
            print(year + "年" + month + "月的收入为：" + str(num) + "元")
            print('入住率为：' + str(rate) + '%')

        elif type == "3":
            year = input("请输入年份：")
            month = input("请输入月份：")
            room_type = input("请输入房间类型：")
            num, rate = FinanceChart_Sum_CertainMonth_RoomType(int(year), int(month), room_type)
            print(year + "年" + month + "月" + room_type + "的收入为：" + str(num) + "元")
            print('入住率为：' + str(rate) + '%')



def EMPLOYEE():
    while True:
        print("------------------------------------------------")
        print("                员工信息界面                    ")
        print("\t1--查询员工信息\t 2--修改员工信息")
        print("\t3--添加员工\t 4--删除员工")
        print("\t0--退出当前界面")
        op = input("请选择操作：")

        attri_en = ["e_id", "full_name", "age", "sex", "phone", "address"]
        attri_cn = ["工号", "姓名", "年龄", "性别", "电话", "地址"]


        if op == "0":
            break

        elif op == "1":
            attris = ["e_id", "full_name", "phone", "address"]
            print("查询条件：")
            print("\t1--工号\t 2--姓名")
            print("\t3--电话\t 4--地址")
            print("\t0--退出当前界面")
            index = input("请选择查询条件：")
            index = int(index) - 1
            value = input("请输入查询值：")
            results = EMPLOYEE_QUERY(attris[index], value)
            top = "%s\t\t%s\t%s\t%s\t%s\t\t%s" %(attri_cn[0], attri_cn[1], attri_cn[2], attri_cn[3], attri_cn[4], attri_cn[5])
            print(top)
            for result in results:
                row = "%s\t%s\t%s\t%s\t%s\t%s" %(result[0], result[1], result[2], result[3], result[4], result[5])
                print(row)

            print("---------------------------------------------------")



        elif op == "2":
            EID = input("请输入工号：")
            print("\n可修改属性：")
            print("\t1--姓名\t 2--年龄")
            print("\t3--性别\t 4--电话")
            print("\t5--地址")
            print("\t0--退出当前界面")
            index = input("请选择需要修改的属性：")
            value = input("请输入修改值：")
            index = int(index)
            EMPLOYEE_UPDATE(attri_en[index], value)

            print("修改成功！")


        elif op == "3":
            EID = input("请输入工号：")
            name = input("请输入姓名：")
            age = input("请输入年龄：")
            sex = input("请输入性别：")
            phone = input("请输入电话：")
            address = input("请输入地址：")
            EMPLOYEE_ADD(EID, name, age, sex, phone, address)

            print("添加成功！")

        elif op == "4":
            EID = input("请输入工号：")
            EMPLOYEE_DELETE(EID)
            print("已删除！")


def CUSTOMER():
    while True:
        print("------------------------------------------------")
        print("                客户信息查询界面                    ")
        print("查询条件：")
        print("1--订单号\t\t2--身份证")
        print("3--姓名\t\t4--电话号码")
        print("0--退出当前界面")
        op1 = input("请选择查询条件：")
        if op1 == "0":
            return

        value = input("请输入查询值：")
        index = int(op1) - 1
        attris = ['order_no', 'id', 'customer_name', 'phone']
        results = check_in_query(attris[index], value)
        print("订单号\t\t房间号\t\t身份证\t\t姓名\t电话\t入住时间")
        for res in results:
            print("%s\t%s\t%s\t%s\t%s\t%s"%(res[0], res[1], res[2], res[3], res[4], res[5] + ' ' + res[6]))



def ROOM_STATUS():

    while True:
        print("------------------------------------------------")
        print("                客房查询界面                    ")
        print("温馨提示：选项留空表示该条件为 (all)")
        RID = input("请输入房间号：")
        RType = input("请输入房间类型：")
        RStatus = input("请输入房间状态：")
        start = input("请输入起始日期(2022/1/1)：")
        end = input("请输入终止日期(2022/1/1)：")

        start_list = start.split('/')
        end_list = end.split('/')

        if RID == "":
            RID = 'all'

        if RType == "":
            RType = 'all'

        if RStatus == "":
            RStatus = 'all'

        results = show_room_status_1(int(start_list[0]), int(start_list[1]), int(start_list[2]), int(end_list[0]), int(end_list[1]), int(end_list[2]), RID, RStatus, RType)
        for res in results:
            print("%s\t%s\t%s\t%s\t%s"%(res[0], res[1], res[2], res[3], res[4]))

        print("0--退出当前页面\t1--继续查询")
        op = input("请选择操作：")
        if op == "0":
            break

def VIP_MANAGE():
    while True:
        print("------------------------------------------------")
        print("                VIP信息管理界面                    ")
        print("\t1--查询VIP信息\t 2--修改VIP信息")
        print("\t3--添加VIP\t\t 4--删除VIP")
        print("\t0--退出当前界面")
        op = input("请选择操作：")

        attri_en = ["e_id", "full_name", "age", "sex", "phone", "address"]
        attri_cn = ["身份证号码", "姓名", "性别", "电话", "VIP等级", "折扣", "积分"]


        if op == "0":
            break

        elif op == "1":
            attris = ["id", "phone"]
            print("查询条件：")
            print("\t1--身份证\t 2--电话")
            print("\t0--退出当前界面")
            index = input("请选择查询条件：")
            index = int(index) - 1
            value = input("请输入查询值：")
            results = EMPLOYEE_QUERY(attris[index], value)
            top = "%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s" %(attri_cn[0], attri_cn[1], attri_cn[2], attri_cn[3], attri_cn[4], attri_cn[5], attri_cn[6])
            print(top)
            for result in results:
                row = "%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s" %(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
                print(row)

            print("---------------------------------------------------")



        elif op == "2":
            EID = input("请输入工号：")
            print("\n可修改属性：")
            print("\t1--姓名\t 2--年龄")
            print("\t3--性别\t 4--电话")
            print("\t5--地址")
            print("\t0--退出当前界面")
            index = input("请选择需要修改的属性：")
            value = input("请输入修改值：")
            index = int(index)
            EMPLOYEE_UPDATE(attri_en[index], value)

            print("修改成功！")


        elif op == "3":
            EID = input("请输入工号：")
            name = input("请输入姓名：")
            age = input("请输入年龄：")
            sex = input("请输入性别：")
            phone = input("请输入电话：")
            address = input("请输入地址：")
            EMPLOYEE_ADD(EID, name, age, sex, phone, address)

            print("添加成功！")

        elif op == "4":
            EID = input("请输入工号：")
            EMPLOYEE_DELETE(EID)
            print("已删除！")


def Admin():
    cnt = 0
    global Dealer_ID
    while True:
        print("------------------------------------------------")
        Dealer_ID = input("ID:")
        password = getpass.getpass("password:")
        res = EMPLOYEE_QUERY('e_id', Dealer_ID)

        if len(res) == 0 or password != ADMIN_PASSWORD:
            print("Incorrect ID or password！")
            cnt += 1
            if cnt == 5:
                print("Incorrect Password more than five times! \n System exits!")
                return 0
        else:
            break

    while True:

        print("------------------------------------------------")
        print("                  管理员界面                      ")
        print("                                               ")
        print("                  可选择功能                      ")
        print("\t 1--登记入住\t\t 2--登出结账\t")
        print("\t 3--预订房间\t\t 4--财务报表\t")
        print("\t 5--客户信息查询\t 6--员工信息界面")
        print("\t 7--客房状态查询\t 8--修改房间价格")
        print("\t 9--VIP信息管理\t\t 0--退出")

        print("------------------------------------------------")
        operation = input("请选择操作：")
        print(operation)
        if operation == "0":
            return

        elif operation == "1":
            CHECK_IN()

        elif operation == "2":
            CHECK_OUT()

        elif operation == "3":
            Reservation()

        elif operation == "4":
            FINANCE()

        elif operation == "5":
            CUSTOMER()

        elif operation == "6":
            EMPLOYEE()

        elif operation == "7":
            ROOM_STATUS()

        elif operation == "8":
            UPDATE_PRICE()

        elif operation == "9":
            VIP()


def User():
    cnt = 0
    global Dealer_ID
    while True:
        print("------------------------------------------------")
        Dealer_ID = input("ID:")
        password = getpass.getpass("password:")
        res = EMPLOYEE_QUERY('e_id', Dealer_ID)


        if len(res) == 0 or password != USER_PASSWORD:
            print("Incorrect ID or password！")
            cnt += 1
            if cnt == 5:
                print("Incorrect Password more than five times! \n System exits!")
                return 0
        else:
            break

    while True:

        print("------------------------------------------------")
        print("                  用户界面                      ")
        print("                                               ")
        print("                  可选择功能                      ")
        print("\t 1--登记入住\t\t 2--登出结账\t")
        print("\t 3--预订房间\t\t 4--客户信息查询\t")
        print("\t 5--VIP信息管理\t\t 0--退出\t")
        print("------------------------------------------------")
        operation = input("请选择操作：")
        print(operation)
        if operation == "0":
            return

        elif operation == "1":
            CHECK_IN()

        elif operation == "2":
            CHECK_OUT()

        elif operation == "3":
            Reservation()

        elif operation == "4":
            CUSTOMER()

        elif operation == "5":
            VIP_MANAGE()


def MAX_NO():
    query = 'select max(order_no) from order_list;'
    db = MySQLdb.connect('localhost', 'root', '1234', 'hotel')
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.commit()
    db.close()
    return res[0]

def main():
    global ORDER_NO
    temp = MAX_NO()
    ORDER_NO = int(temp[0]) + 1
    print(ORDER_NO)
    while True:
        print("-------------------------------------------------")
        print("|   Welcome to the Hotel Management System      |")
        print("|      Please choose the next operation         |")
        print("|                                               |")
        print("|   1--Admin login   2--User login    0--exit   |")
        print("|                                               |")
        print("-------------------------------------------------")
        operation = input("请选择操作：")
        if operation == "0":
            return

        elif operation == "1":
            Admin()

        else:
            User()


if __name__ == "__main__":
    main()

