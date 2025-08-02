
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
cursor.execute("create database if not exists maojie;")
conn.select_db("maojie") # 建立与数据库的连接

# 创建学生信息表， 若有则不创建
cursor.execute("""CREATE TABLE IF NOT EXISTS students(
    id int,
    name varchar(10),
    type int,
    source varchae(20),
    money int,
    data,varchar(20)
);""")


# 创建账号密码表，若有则不创建
cursor.execute("""CREATE TABLE IF NOT EXISTS admin_name_pwd(
    name varchar(10),
    pwd varchar(10)
);""")


# 判断登录的账号密码是否都正确
def check_login(uname, pwd):
    cursor.execute("select * from admin_name_pwd")
    results = cursor.fetchall()
    # print(results)
    for na, pd in results:
        if na == uname and pd == pwd:
            return True, '登录成功'
    return False, '登录失败,账号或密码错误'

# 添加正确注册的账号以及密码
def add_admin_name_pwd(uname, pwd):
    cursor.execute("insert into admin_name_pwd values('{0}', '{1}');".format(uname, pwd))
# add_admin_name_pwd("123", "123")

# 检验注册的账号名称是否已经存在
def check_usname(uname):
    cursor.execute("select count(*) from admin_name_pwd anp where name = '{0}';".format(uname))
    res = cursor.fetchall()
    if res[0][0]:
        return True
    return False


# 获取数据库中学生所有信息，按给定的信息给出
# 通过全局变量sort_data以及sort_student
# sort_student 为0代表升序，为一代表降序
def all():
    if sort_student == 1:
        if sort_data == 0:
            cursor.execute("select * from students order by id;")
        elif sort_data == 1:
            cursor.execute("select * from students order by type;")
        elif sort_data == 2:
            cursor.execute("select * from students order by money;")
        elif sort_data == 3:
            cursor.execute("select * from students order by data;")
    else:
        if sort_data == 0:
            cursor.execute("select * from students order by id desc;")
        elif sort_data == 1:
            cursor.execute("select * from students order by type desc;")
        elif sort_data == 2:
            cursor.execute("select * from students order by money desc;")
        elif sort_data == 3:
            cursor.execute("select * from students order by data desc;")
    data = cursor.fetchall()
    key = ('id', 'name', 'type', 'source', 'money', 'data')
    jsonList = []
    # 通过数据得到的数据是元组类型，需要压缩成字典类型便于输出
    for i in data:
        jsonList.append(dict(zip(key, i)))
    return jsonList

# 查询录入的学号是否存在

# 单独查询某个班级的成绩
def search_kulas(kulas_value):
    cursor.execute("select * from students where kulas = '{0}';".format(kulas_value))
    data = cursor.fetchall()
    key = ('id', 'name', 'kulas', 'math', 'english', 'computer', 'total')
    jsonList = []
    # 通过数据得到的数据是元组类型，需要压缩成字典类型便于输出
    for i in data:
        jsonList.append(dict(zip(key, i)))
    return jsonList
# 插入一条学生信息
def insert(stu):
    cursor.execute("SELECT MAX(id) FROM students;")
    max_id = cursor.fetchone()[0]
    new_id = 1 if max_id is None else max_id + 1
    cursor.execute("INSERT INTO students (id, name, kulas, math, english, computer, total) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                   (new_id, stu[1], stu[2], stu[3], stu[4], stu[5], stu[6]))

# 通过id来删除学生信息
def delete_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("delete from students where id = '{0}';".format(user_id))
        return True, '删除成功'
    else: return False, '学号为' + str(user_id) + '的学生不存在'

# 通过名字来删除学生信息
def delete_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    # print(res)
    if res[0][0]:
        cursor.execute("delete from students where name = '{0}';".format(user_name))
        return True, '删除成功'
    else: return False, '姓名为' + str(user_name) + '的学生不存在'


# 通过id来查询学生的信息
def search_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where id = '{0}';".format(user_id))
        stu = cursor.fetchall()
        return True, stu
    else:
        return False, '学号为' + str(user_id) + '的学生不存在'

# 通过学生姓名来查询剩余的信息
def search_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where name = '{0}';".format(user_name))
        stu = cursor.fetchall()
        return True, stu
    else:
        return False, '名字为' + str(user_name) + '的学生不存在'
def get_max_id():
    # 假设你已经连接到数据库，并且有一个 cursor 对象
    cursor.execute("SELECT MAX(id) FROM students")  # 查询最大学号
    result = cursor.fetchone()
    if result[0] is None:  # 如果数据库为空，返回初始学号 1
        return 1
    else:
        return result[0]
# 下面内容是初始化数据库，不过需要手动解开注释
tuple = (
         (20, '徐寒研', '软件开发4班', 68, 59, 86, 213),
         (19, '荣浩博', '软件开发4班', 56, 83, 20, 159),
         (18, '刘德泽', '软件开发4班', 78, 83, 89, 250),
         (17, '陈涵梁', '软件开发4班', 68, 99, 67, 234),
         (16, '宋明玉', '软件开发4班', 79, 72, 90, 241),
         (15, '邓海洋', '软件开发4班', 68, 47, 89, 204),
         (14, '快乐男孩', '软件开发4班', 79, 78, 48, 205),
         (13, '周解青', '软件开发4班', 69, 78, 82, 229),
         (12, '帅哥', '软件开发4班', 72, 47, 88, 207),
         (11, '金十一', '物联网3班', 84, 68, 92, 244),
         (10, '郑十', '物联网2班', 81, 75, 88, 244),
         (9, '吴九', '大数据1班', 92, 87, 61, 240),
         (8, '周八', '软件土木3班', 87, 71, 92, 250),
         (7, '孙七', '计算机1班', 64, 76, 83, 223),
         (6, '赵六', '软件开发4班', 48, 86, 75, 209),
         (5, '王五', '软件金融2班', 78, 92, 62, 232),
         (4, '李四', '软件会计2班', 80, 83, 45, 208),
         (3, '张三', '软件土木5班', 61, 72, 77, 210),
         (2, '陈二', '计算机5班', 81, 67, 72, 220),
         (1, '刘一', '软件开发4班', 60, 85, 67, 212))

# 手动解除即可将这些信息添加进数据库中，使用之后需重新注释
"""
# 往student中加入信息，若有则不加入
for stu in tuple:
    if check_student_id(stu[0])[0] == True:
        insert(stu)
"""
# 加入初始账号，若有则不加入
if check_usname("root") == False:
    add_admin_name_pwd('root', 'root')
