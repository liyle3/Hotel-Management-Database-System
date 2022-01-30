import MySQLdb
def VIP_QUERY(attr, value):
    """
    根据id or phone检查会员信息是否存在
    """

    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)
    query = "select * from VIP where " + attr + "='" + value + "';"
    cursor = db.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    return res


def VIP_ADD(ID, name, sex, phone):
    """添加会员信息"""

    query = "insert VIP values('" + ID \
                 + "', '" + name + "', '" + sex + "', '" \
                 + phone  + "', 1, 0.9, 0);"
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(query)
        # 提交到数据库执行
        db.commit()

    except:
        # 发生错误时回滚
        db.rollback()

    db.close()




def VIP_UPDATE(attr1, value1, attr2, value2):
    """
    更新会员信息
    """
    query = "update VIP set " + attr2 + " = '" + value2 + "' where " + attr1 + " = '" + value1 + "';"
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)
    cursor = db.cursor()

    try:
        # 执行sql语句
        cursor.execute(query)
        # 提交到数据库执行
        db.commit()

    except:
        # 发生错误时回滚
        db.rollback()

    db.close()



def VIP_DELETE(attr, value):
    """
    仅支持根据身份证号码和电话进行删除
    """
    query = "delete from VIP where " + attr + " = '" + value + "';"
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)
    cursor = db.cursor()

    try:
        # 执行sql语句
        cursor.execute(query)
        # 提交到数据库执行
        db.commit()

    except:
        # 发生错误时回滚
        db.rollback()

    db.close()



def VIP_POINT(id, spent):

    result = VIP_QUERY("id", id)
    if len(result) == 0:
        # 该用户不是VIP
        return
    res = result[0]
    points = int(res[-1]) + int(spent)
    cur_level = int(res[-3])
    new_level = int(points / 1000) + 1
    VIP_UPDATE("id", id, "integration", str(points))

    if cur_level < new_level:
        VIP_UPDATE("id", id, "cur_level", str(new_level))
        discount = 0.9

        if new_level < 10:
            discount = 0.95 - 0.05 * new_level

        else:
            discount = 0.5

        VIP_UPDATE("id", id, "discount", str(discount))



# VIP_POINT('440823202201012312', 588.0)

