from tkinter import *
import pymysql
# 创建连接数据库student的对象conn
conn = pymysql.connect(
    host='localhost',  # 数据库主机名
    port=3306,  # 数据库端口号，默认为3306
    user='root',  # 数据库用户名
    password='110119',  # 数据库密s\
    autocommit=True  # 设置修改数据无需确认
)
# 获取游标对象
sort_student = int(0)
sort_data = int(0)

cursor = conn.cursor()

# 创建数据库，若有则不创建
cursor.execute("create database if not exists cashmanagement;")
conn.select_db("cashmanagement") # 建立与数据库的连接

# 创建学生信息表， 若有则不创建
cursor.execute("""CREATE TABLE IF NOT EXISTS students(
    id int PRIMARY KEY,
    name varchar(10),
    type int,
    source varchar(20),
    money_in decimal(17,6),
    money_out decimal(17,6),
    date varchar(20)
);""")
 
 
 
 

# 获取数据库中学生所有信息，按给定的信息给出
# 通过全局变量sort_data以及sort_student
# sort_student 为0代表升序，为一代表降序
def all():
    """
    查询并排序学生信息。
    :param sort_student: 排序顺序（1 表示升序，其他值表示降序）
    :param sort_data: 排序字段（0: id, 1: type, 2: money, 3: date）
    :return: 查询结果的 JSON 列表
    """
    # 定义排序字段
    sort_columns = {
        0: "id",
        1: "type",
        2: "money_in",
        3: "money_out",    
        4: "date"
    }

    # 获取排序字段和排序顺序
    sort_column = sort_columns.get(sort_data, "id")  # 默认按 id 排序
    sort_order = "ASC" if sort_student == 1 else "DESC"

    # 构造 SQL 查询语句
    query = f"SELECT * FROM students ORDER BY {sort_column} {sort_order};"

    # 执行查询
    cursor.execute(query)
    data = cursor.fetchall()

    # 定义字段名
    key = ('id', 'name', 'type', 'source', 'money_in','money_out','date')

    # 将查询结果转换为字典格式
    jsonList = [dict(zip(key, i)) for i in data]
    return jsonList

 
 
data = [
    (20, '徐寒研', 4, '软件开发4班', 68, '2024.01.01'),
    (19, '荣浩博', 4, '软件开发4班', 56, '2024.01.02'),
    (18, '刘德泽', 4, '软件开发4班', 78, '2024.01.03'),
    (17, '陈涵梁', 4, '软件开发4班', 68, '2024.01.04'),
    (16, '宋明玉', 4, '软件开发4班', 79, '2024.01.05'),
    (15, '邓海洋', 4, '软件开发4班', 68, '2024.01.06'),
    (14, '快乐男孩', 4, '软件开发4班', 79, '2024.01.07'),
    (13, '周解青', 4, '软件开发4班', 69, '2024.01.08'),
    (12, '帅哥', 4, '软件开发4班', 72, '2024.01.09'),
    (11, '金十一', 3, '物联网3班', 84, '2024.01.10'),
    (10, '郑十', 2, '物联网2班', 81, '2024.01.11'),
    (9, '吴九', 1, '大数据1班', 92, '2024.01.12'),
    (8, '周八', 3, '软件土木3班', 87, '2024.01.13'),
    (7, '孙七', 1, '计算机1班', 64, '2024.01.14'),
    (6, '赵六', 4, '软件开发4班', 48, '2024.01.15'),
    (5, '王五', 2, '软件金融2班', 78, '2024.01.16'),
    (4, '李四', 2, '软件会计2班', 80, '2024.01.17'),
    (3, '张三', 5, '软件土木5班', 61, '2024.01.18'),
    (2, '陈二', 5, '计算机5班', 81, '2024.01.19'),
    (1, '刘一', 4, '软件开发4班', 60, '2024.01.20')
]
# def insert(stu):
#     cursor.execute("insert into students values('{0}', '{1}', '{2}','{3}', '{4}', '{5}', '{6}');".
#                    format(stu[0], stu[1], stu[2], stu[3], stu[4], stu[5], stu[6]))
# def insert(stu):
#     # 参数化查询，避免 SQL 注入
#     query = "INSERT INTO students (id, name, type, source, money, data) VALUES (?, ?, ?, ?, ?, ?);"
#     cursor.execute(query, stu[:6])  # 确保只传递前 6 个值
def insert(stu):
    # 确保 stu 至少有 6 个字段
    if len(stu) < 7:
        raise ValueError(f"stu must have at least 6 fields, but got {len(stu)} fields: {stu}")

    query = "INSERT INTO students (id, name, type, source, money_in,money_out, date) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, stu[:7])  # 确保只传递前 6 个值

#插入模拟数据
# for stu in data:
#     insert(stu)
# 通过学生姓名来查询信息
def search_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where name = '{0}';".format(user_name))
        stu = cursor.fetchall()
        return True, stu
    else:
        return False, '名字为' + str(user_name) + '的人不存在'
# 通过id来查询人的信息
def search_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where id = '{0}';".format(user_id))
        stu = cursor.fetchall()
        return True, stu
    else:
        return False, '序号为' + str(user_id) + '的人不存在'
 
def delete_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("delete from students where id = '{0}';".format(user_id))
        cursor.execute("UPDATE students SET id = id - 1 WHERE id > %s;", (user_id,))
        return True, '删除成功'
    else: return False, '序号为' + str(user_id) + '的人不存在'

def delete_id2(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("delete from students where id = '{0}';".format(user_id))
        return True, '删除成功'
    else: return False, '序号为' + str(user_id) + '的人不存在'
# 通过名字来删除学生信息
def delete_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    # print(res)
    if res[0][0]:
        cursor.execute("delete from students where name = '{0}';".format(user_name))
       # cursor.execute("UPDATE students SET id = id - 1 WHERE id > %s;", (,))
        return True, '删除成功'
    else: return False, '姓名为' + str(user_name) + '的人不存在'
# 单独查询某个类别的人
def search_type(type):
    cursor.execute("select * from students where type = '{0}';".format(type))
    data = cursor.fetchall()
    key = ('id', 'name', 'type', 'source', 'money_in','money_out' 'date')
    jsonList = []
    # 通过数据得到的数据是元组类型，需要压缩成字典类型便于输出
    for i in data:
        jsonList.append(dict(zip(key, i)))
    return jsonList





 
import mysql.connector
def search_date(startdate, enddate):
    """
    查询在日期范围 startdate 到 enddate 之间的学生数据。
    :param startdate: 起始日期（字符串，格式为 YYYY.MM.DD）
    :param enddate: 结束日期（字符串，格式为 YYYY.MM.DD）
    :return: 查询结果的 JSON 列表，或者提示信息
    """
    # 检查日期格式是否正确
    try:
        # 确保日期格式符合 YYYY.MM.DD
        startdate = str(startdate)
        enddate = str(enddate)
        if len(startdate) != 10 or len(enddate) != 10 or startdate[4] != '.' or startdate[7] != '.' or enddate[4] != '.' or enddate[7] != '.':
            raise ValueError
    except ValueError:
        return "输入的日期格式无效，请按照 YYYY.MM.DD 的格式输入。"

    # 构造 SQL 查询语句
    query = "SELECT * FROM students WHERE date BETWEEN %s AND %s;"
    cursor.execute(query, (startdate, enddate))
    data = cursor.fetchall()

    if not data:
        return f"在日期范围 {startdate} 到 {enddate} 之间没有找到数据。"

    # 定义字段名，确保与数据库中的字段一致
    key = ('id', 'name', 'type', 'source', 'money', 'date')
    jsonList = [dict(zip(key, i)) for i in data]
    return jsonList
def search_money(a, b):
    """
    查询在金钱范围 a 到 b 之间的学生数据。
    :param a: 起始金额（整数或浮点数）
    :param b: 结束金额（整数或浮点数）
    :return: 查询结果的 JSON 列表，或者提示信息
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return "输入的金额范围无效，请输入数字。"

    query = "SELECT * FROM students WHERE money BETWEEN %s AND %s;"
    cursor.execute(query, (a, b))
    data = cursor.fetchall()

    if not data:
        return f"在金额范围 {a} 到 {b} 之间没有找到数据。"

    key = ('id', 'name', 'type', 'source', 'money', 'date')  # 确保字段名与数据库一致
    jsonList = [dict(zip(key, i)) for i in data]
    return jsonList
 
 
 
 
#获取数据条数
def get_max_id():
    # query = "SELECT MAX(id) FROM students"
    query = "SELECT count(*) FROM students"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result[0] else 0

def get_min_money():
    query = "SELECT MIN(money_in+money_out) FROM students"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def get_max_money():
    query = "SELECT MAX(money_in+money_out) FROM students"
    cursor.execute(query)
    result = cursor.fetchone()
#     return result[0] if result[0] is not None else 0
def get_min_date():
    query = "SELECT MIN(date) FROM students"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result[0] is not None else None
  
# def search(type_name=None,type_value=None, min_money=None, max_money=None, start_date=None, end_date=None):
#     query = "SELECT * FROM students WHERE 1=1"
#     params = []
#     if type_name:
#         query += " AND date <= %s"
#         params.append(end_date)
#     if type_value:
#         query += " AND type = %s"
#         params.append(type_value)
#     if min_money:
#         query += " AND money >= %s"
#         params.append(min_money)
#     if max_money:
#         query += " AND money <= %s"
#         params.append(max_money)
#     if start_date:
#         query += " AND date >= %s"
#         params.append(start_date)
#     if end_date:
#         query += " AND date <= %s"
#         params.append(end_date)
    

#     cursor.execute(query, params)
#     result = cursor.fetchall()  # 返回一个包含 tuple 的列表
#     print("Debug: Database result =", result)  # 打印数据库查询结果
#     return result
# def search(type_name=None, type_value=None,
#            min_money=None, max_money=None,
#            start_date=None, end_date=None,
#            name=None,           # 新增：姓名查询
#            fuzzy=True):         # 新增：是否启用模糊查询
#     """
#     查询 students 表
#     :param fuzzy: True 表示模糊匹配姓名，False 表示精确匹配
#     """
#     query = "SELECT * FROM students WHERE 1=1"
#     params = []

#     if name:
#         if fuzzy:
#             query += " AND name LIKE %s"
#             params.append(f"%{name}%")
#         else:
#             query += " AND name = %s"
#             params.append(name)

#     if type_value:
#         query += " AND type = %s"
#         params.append(type_value)
#     if min_money:
#         query += " AND money >= %s"
#         params.append(min_money)
#     if max_money:
#         query += " AND money <= %s"
#         params.append(max_money)
#     if start_date:
#         query += " AND date >= %s"
#         params.append(start_date)
#     if end_date:
#         query += " AND date <= %s"
#         params.append(end_date)

#     cursor.execute(query, params)
#     result = cursor.fetchall()
#     print("Debug: Database result =", result)
#     return result
@staticmethod
def search(mode=0, name_key=None, type_value=None,
           min_money=0, max_money=999999999,
           start_date=None, end_date=None):
    """
    mode: 0全部 1收入 -1支出
    """
    sql = """
        SELECT id, name, type, source,
               COALESCE(money_in, 0)  AS money_in,
               COALESCE(money_out, 0) AS money_out,
               date
        FROM students
        WHERE 1=1
    """
    params = []

    # 姓名模糊
    if name_key:
        sql += " AND name LIKE %s"
        params.append(f'%{name_key}%')

    # 类型精确
    if type_value:
        sql += " AND type = %s"
        params.append(type_value)

    # 收支模式
    if mode == 1:          # 只保留收入
        sql += " AND money_in > 0"
    elif mode == -1:       # 只保留支出
        sql += " AND money_out > 0"

    # 金额区间（money_in + money_out）
    sql += " AND (money_in + money_out) BETWEEN %s AND %s"
    params.extend([min_money, max_money])

    # 日期区间
    if start_date:
        sql += " AND date >= %s"
        params.append(start_date)
    if end_date:
        sql += " AND date <= %s"
        params.append(end_date)

    sql += " ORDER BY id DESC"

    cursor.execute(sql, params)
    return cursor.fetchall()

def update_student(student_id, new_data):
    try:
        

        # 构造 SQL 更新语句
        sql = """
        UPDATE students
        SET name = %s, type = %s, source = %s, money = %s, date = %s
        WHERE id = %s
        """
        # 注意：new_data 的顺序需要与 SQL 中的字段顺序一致
        cursor.execute(sql, (*new_data, student_id))
        conn.commit()

        if cursor.rowcount > 0:
            return True, "学生信息更新成功"
        else:
            return False, "未找到指定的学生信息"
    except Exception as e:
        return False, f"更新失败：{e}"
  