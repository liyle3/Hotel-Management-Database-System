import MySQLdb


def EMPLOYEE_QUERY(attr, value):
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)
    query = "select * from employee where %s = '%s';" %(attr, value)
    cursor = db.cursor()
    cursor.execute(query)
    # 提交到数据库执行
    res = cursor.fetchall()
    db.close()
    return res

def EMPLOYEE_UPDATE(attr, value):
    query = "update table set " + attr + " = '" + value + "';"
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)

    try:
        # 执行sql语句
        db.cursor.execute(query)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    db.close()

def EMPLOYEE_ADD(ID, name, age, sex, phone, address):
    query = "insert into table employee values('" + ID \
                 + "', '" + name + "', '" + age + "', '" \
                 + sex + "', '" + phone + "', '" + address + "';"
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)

    try:
        # 执行sql语句
        db.cursor.execute(query)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    db.close()

def EMPLOYEE_DELETE(EID):
    query = "delete from employee where e_id = '" + EID + "';"
    db = MySQLdb.connect("localhost", "root", "1234", "hotel", port=3306, autocommit=True)

    try:
        # 执行sql语句
        db.cursor.execute(query)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    db.close()

