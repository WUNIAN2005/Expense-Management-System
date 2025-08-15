from tkinter import *
from tkinter import ttk
import mysql_student
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime  # 导入 datetime 模块
import re
from decimal import Decimal
from decimal import Decimal, InvalidOperation
current_date = datetime.now().strftime("%Y.%m.%d")
allminmoney_in=mysql_student.get_min_money()
allmaxmoney=mysql_student.get_max_money()
min_date=mysql_student.get_min_date()


# # 实现录入页面的类
# class InsertFrame(Frame):
#     def __init__(self, root):
#         super().__init__(root)
#         self.id = StringVar()
#         self.name = StringVar()
#         self.type = StringVar()
#         self.source = StringVar()
#         self.money = StringVar()
#         self.date = StringVar()
       
       

#         # 打印录入是否成功信息
#         self.status_insert = StringVar()
#         self.insert_page()

#     # 打印修输入的项目以及输入框
#     def insert_page(self):
#         # Label(self, text='学   号 : ').grid(row=1, column=1, pady=5)
#         # self.entry_id = Entry(self, textvariable=self.id)
#         # self.entry_id.grid(row=1, column=2, pady=5)

#         Label(self, text='姓   名 : ').grid(row=2, column=1, pady=5)
#         self.entry_name = Entry(self, textvariable=self.name)
#         self.entry_name.grid(row=2, column=2, pady=5)

#         Label(self, text='类 别 : ').grid(row=3, column=1, pady=5)
#         self.entry_type = Entry(self, textvariable=self.type)
#         self.entry_type.grid(row=3, column=2, pady=5)

#         Label(self, text='公 司 : ').grid(row=4, column=1, pady=5)
#         self.entry_source = Entry(self, textvariable=self.source)
#         self.entry_source.grid(row=4, column=2, pady=5)

#         Label(self, text='金 额 : ').grid(row=5, column=1, pady=5)
#         self.entry_money = Entry(self, textvariable=self.money)
#         self.entry_money.grid(row=5, column=2, pady=5)

#         Label(self, text='日 期 : ').grid(row=6, column=1, pady=5)
#         self.entry_date = Entry(self, textvariable=self.date)
#         self.entry_date.grid(row=6, column=2, pady=5)

#         Button(self, text='清空', command=self.insert_deleteValue).grid(row=7, column=1, pady=10)
#         Button(self, text='录入', command=self.insert_data).grid(row=7, column=3, pady=10)

#         # Label(self, textvariable=self.status_insert,fg='red').grid(row=8, column=2, padx=10)
#         self.status_label = Label(self, textvariable=self.status_insert, fg='red')
#         self.status_label.grid(row=8, column=2, padx=10)
# class InsertFrame(Frame):
#     def __init__(self, root):
#         super().__init__(root)
#         self.id = StringVar()
#         self.name = StringVar()
#         self.type = StringVar()
#         self.source = StringVar()
#         self.money_in = StringVar()
#         self.money_out=StringVar()
#         self.date = StringVar()
#         self.status_insert = StringVar()
#         self.insert_page()

#     def insert_page(self):
#         # 让 Frame 的行和列可扩展
#         for i in range(1, 9):  # 行 1-8
#             self.grid_rowconfigure(i, weight=1)
#         for j in range(1, 4):  # 列 1-3
#             self.grid_columnconfigure(j, weight=1)

#         # 使用 sticky="ew" 让 Entry 控件水平填充
#         Label(self, text='姓   名 : ').grid(row=2, column=1, pady=5, sticky="e")
#         self.entry_name = Entry(self, textvariable=self.name)
#         self.entry_name.grid(row=2, column=2, pady=5, sticky="ew")

#         Label(self, text='类 别 : ').grid(row=3, column=1, pady=5, sticky="e")
#         self.entry_type = Entry(self, textvariable=self.type)
#         self.entry_type.grid(row=3, column=2, pady=5, sticky="ew")

#         Label(self, text='公 司 : ').grid(row=4, column=1, pady=5, sticky="e")
#         self.entry_source = Entry(self, textvariable=self.source)
#         self.entry_source.grid(row=4, column=2, pady=5, sticky="ew")

#         Label(self, text='金 额 : ').grid(row=5, column=1, pady=5, sticky="e")
#         self.entry_money = Entry(self, textvariable=self.money)
#         self.entry_money.grid(row=5, column=2, pady=5, sticky="ew")

#         Label(self, text='日 期 : ').grid(row=6, column=1, pady=5, sticky="e")
#         self.entry_date = Entry(self, textvariable=self.date)
#         self.entry_date.grid(row=6, column=2, pady=5, sticky="ew")

#         Button(self, text='清空', command=self.insert_deleteValue).grid(row=7, column=1, pady=10, sticky="e")
#         Button(self, text='录入', command=self.insert_data).grid(row=7, column=3, pady=10, sticky="w")

#         self.status_label = Label(self, textvariable=self.status_insert, fg='red')
#         self.status_label.grid(row=8, column=2, padx=10, sticky="ew")

#        # 删除输入框中的内容
#     def insert_deleteValue(self):
#         #self.entry_id.delete(0, END)
#         self.entry_name.delete(0, END)
#         self.entry_type.delete(0, END)
#         self.entry_source.delete(0, END)
#         self.entry_money.delete(0, END)
#         self.entry_date.delete(0, END)

  
#     def insert_data(self):
#         if not self.name.get():
#             self.insert_name = 'NULL'
#         else:
#             self.insert_name = self.name.get()

#         if not self.type.get():
#             self.insert_type = 'NULL'
#         else:
#             self.insert_type = self.type.get()

#         if not self.source.get():
#             self.insert_source = 'NULL'
#         else:
#             self.insert_source = self.source.get()

#         if not self.money.get():
#             self.insert_money =decimal(0)
#         else:
#             self.insert_money = self.money.get()

#         if not self.date.get():
#             self.insert_date = current_date  # 假设 current_date 是一个全局变量
#         else:
#             try:
#                 # 将输入的日期转换为 datetime 对象，并格式化为标准格式
#                 self.insert_date = datetime.strptime(self.date.get(), "%Y.%m.%d").strftime("%Y.%m.%d")
#             except ValueError:
#                 # 如果用户输入的日期格式不正确，提示错误
#                 self.status_insert.set("日期格式错误，请输入 YYYY.MM.DD 格式的日期")
#                 return

#         # 获取最大 ID 并加 1
#         a = mysql_student.get_max_id() + 1
#         stu = (a, self.insert_name, self.insert_type, self.insert_source,
#             self.insert_money, self.insert_date)

#         # 尝试插入数据
#         # try:
#         #     mysql_student.insert(stu)  # 这一部分为存在并导入信息
#         #     self.status_insert.set("录入成功")  # 显示录入成功的信息
#         # except Exception as e:
#         #     self.status_insert.set(f"录入失败：{e}")  # 如果插入失败，显示错误信息
#         try:
#             mysql_student.insert(stu)  # 这一部分为存在并导入信息
#             self.status_insert.set("录入成功")  # 显示录入成功的信息
#             self.status_label.after(3000, lambda: self.status_insert.set(""))  # 3秒后清除信息
#         except Exception as e:
#             self.status_insert.set(f"录入失败：{e}")  # 如果插入失败，显示错误信息
#             self.status_label.after(20000, lambda: self.status_insert.set(""))  # 3秒后清除信息
# 实现录入页面的类
# 1️⃣  把 ThousandsEntry 粘到文件末尾（任何地方都行）
# from decimal import Decimal
# import re
# class ThousandsEntry(Entry):
#     def __init__(self, master, textvariable=None, **kw):
#         super().__init__(master, textvariable=textvariable, **kw)
#         self.bind('<KeyRelease>', self._fmt)
#         self.bind('<FocusOut>',   self._fmt)
#     def _fmt(self, ev=None):
#         raw = self.get().replace(',', '')  # 去掉逗号
#         if '.' in raw:
#             parts = raw.split('.')
#             # 检查小数部分是否为空或正在输入中
#             if len(parts[1]) > 6:  # 限制小数点后最多六位
#                 return
#             if parts[0].isdigit() and parts[1].isdigit():
#                 fmt = f"{int(parts[0]):,}.{parts[1]}"
#             else:
#                 fmt = raw  # 如果包含非数字字符，不格式化
#         else:
#             if raw.isdigit():
#                 fmt = f"{int(raw):,}"
#             else:
#                 fmt = raw  # 如果包含非数字字符，不格式化

#         if fmt != self.get():
#             self.delete(0, 'end')
#             self.insert(0, fmt)
#     def get_number(self):
#         raw = self.get().strip().replace(',', '')  # 去除可能的前后空格和逗号
#         if raw.isdigit():
#             return Decimal(raw)
#         return 0  # 如果输入无效，返回 0 
from decimal import Decimal, InvalidOperation

class ThousandsEntry(Entry):
    def __init__(self, master, textvariable=None, **kw):
        super().__init__(master, textvariable=textvariable, **kw)
        self.bind('<KeyRelease>', self._fmt)
        self.bind('<FocusOut>', self._fmt)

    def _fmt(self, ev=None):
        raw = self.get().replace(',', '')  # 去掉逗号
        if '.' in raw:
            parts = raw.split('.')
            if len(parts[1]) > 6:  # 限制小数点后最多六位
                return
            if parts[0].isdigit() and parts[1].isdigit():
                fmt = f"{int(parts[0]):,}.{parts[1]}"
            else:
                fmt = raw  # 如果包含非数字字符，不格式化
        else:
            if raw.isdigit():
                fmt = f"{int(raw):,}"
            else:
                fmt = raw  # 如果包含非数字字符，不格式化

        if fmt != self.get():
            self.delete(0, 'end')
            self.insert(0, fmt)

    def get_number(self):
        raw = self.get().strip().replace(',', '')  # 去除可能的前后空格和逗号
        try:
            # 尝试将字符串转换为 Decimal
            return Decimal(raw)
        except InvalidOperation:
            # 如果转换失败，返回 0
            return Decimal('0')
        except Exception as e:
            # 捕获其他可能的异常，并打印错误信息
            print(f"Error converting to Decimal: {e}")
            return Decimal('0')
class InsertFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.id = StringVar()
        self.name = StringVar()
        self.type = StringVar()
        self.source = StringVar()
        self.money_in = StringVar()
        self.money_out=StringVar()
        self.date = StringVar()
       
       

        # 打印录入是否成功信息
        self.status_insert = StringVar()
        self.insert_page()

    # 打印修输入的项目以及输入框
    def insert_page(self):
        # Label(self, text='学   号 : ').grid(row=1, column=1, pady=5)
        # self.entry_id = Entry(self, textvariable=self.id)
        # self.entry_id.grid(row=1, column=2, pady=5)

        Label(self, text='姓   名 : ').grid(row=2, column=1, pady=5)
        self.entry_name = Entry(self, textvariable=self.name)
        self.entry_name.grid(row=2, column=2, pady=5)

        Label(self, text='类 别 : ').grid(row=3, column=1, pady=5)
        self.entry_type = Entry(self, textvariable=self.type)
        self.entry_type.grid(row=3, column=2, pady=5)

        Label(self, text='公 司 : ').grid(row=4, column=1, pady=5)
        self.entry_source = Entry(self, textvariable=self.source)
        self.entry_source.grid(row=4, column=2, pady=5)

        Label(self, text='收 入 金 额 : ').grid(row=5, column=1, pady=5)
        # self.entry_money_in = Entry(self, textvariable=self.money_in)
        self.entry_money_in  = ThousandsEntry(self, textvariable=self.money_in)
        self.entry_money_in.grid(row=5, column=2, pady=5)

        Label(self, text='支 出 金 额 : ').grid(row=6, column=1, pady=5)
        # self.entry_money_out = Entry(self, textvariable=self.money_out)
        self.entry_money_out = ThousandsEntry(self, textvariable=self.money_out)    
        self.entry_money_out.grid(row=6, column=2, pady=5)

        Label(self, text='日 期 : ').grid(row=7, column=1, pady=5)
        self.entry_date = Entry(self, textvariable=self.date)
        self.entry_date.grid(row=7, column=2, pady=5)

        Button(self, text='清空', command=self.insert_deleteValue).grid(row=8, column=1, pady=10)
        Button(self, text='录入', command=self.insert_data).grid(row=8, column=3, pady=10)

        # Label(self, textvariable=self.status_insert,fg='red').grid(row=8, column=2, padx=10)
        self.status_label = Label(self, textvariable=self.status_insert, fg='red')
        self.status_label.grid(row=8, column=2, padx=10)

       # 删除输入框中的内容
    def insert_deleteValue(self):
        #self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_type.delete(0, END)
        self.entry_source.delete(0, END)
        self.entry_money_in.delete(0, END)
        self.entry_money_out.delete(0, END)
        self.entry_date.delete(0, END)

  
    # def insert_data(self):
    #     if not self.name.get():
    #         self.insert_name = 'NULL'
    #     else:
    #         self.insert_name = self.name.get()

    #     if not self.type.get():
    #         self.insert_type = 'NULL'
    #     else:
    #         self.insert_type = self.type.get()

    #     if not self.source.get():
    #         self.insert_source = 'NULL'
    #     else:
    #         self.insert_source = self.source.get()

    #     if not self.money.get():
    #         self.insert_money =float(0)
    #     else:
    #         self.insert_money = self.money.get()

    #     if not self.date.get():
    #         self.insert_date = current_date  # 假设 current_date 是一个全局变量
    #     else:
    #         try:
    #             # 将输入的日期转换为 datetime 对象，并格式化为标准格式
    #             self.insert_date = datetime.strptime(self.date.get(), "%Y.%m.%d").strftime("%Y.%m.%d")
    #         except ValueError:
    #             # 如果用户输入的日期格式不正确，提示错误
    #             self.status_insert.set("日期格式错误，请输入 YYYY.MM.DD 格式的日期")
    #             return

    #     # 获取最大 ID 并加 1
    #     a = mysql_student.get_max_id() + 1
    #     stu = (a, self.insert_name, self.insert_type, self.insert_source,
    #         self.insert_money, self.insert_date)

    #     # 尝试插入数据
    #     # try:
    #     #     mysql_student.insert(stu)  # 这一部分为存在并导入信息
    #     #     self.status_insert.set("录入成功")  # 显示录入成功的信息
    #     # except Exception as e:
    #     #     self.status_insert.set(f"录入失败：{e}")  # 如果插入失败，显示错误信息
    #     try:
    #         mysql_student.insert(stu)  # 这一部分为存在并导入信息
    #         self.status_insert.set("录入成功")  # 显示录入成功的信息
    #         self.status_label.after(3000, lambda: self.status_insert.set(""))  # 3秒后清除信息
    #     except Exception as e:
    #         self.status_insert.set(f"录入失败：{e}")  # 如果插入失败，显示错误信息
    #         self.status_label.after(20000, lambda: self.status_insert.set(""))  # 3秒后清除信息

    def insert_data(self):
        # ---------- 基础字段 ----------
        name   = self.name.get().strip()   or 'NULL'
        type_  = self.type.get().strip()   or 'NULL'
        source = self.source.get().strip() or 'NULL'

       # ---------- 金额：只能填 money_in 或 money_out 中的一项 ----------
        try:    
            # money_in  = Decimal(str(self.entry_money_in.get_number()))
            # money_out = Decimal(str(self.entry_money_out.get_number()))
            # print(money_in)
            money_in = self.entry_money_in.get_number()
            money_out = self.entry_money_out.get_number()

        # 转换为 Decimal
            money_in = Decimal(str(money_in))
            money_out = Decimal(str(money_out))
            print(money_in)
        except ValueError:
            self.status_insert.set("金额必须是数字！")  
            return

        # 业务校验：二者只能有一个大于 0
        if money_in and money_out:
            self.status_insert.set("收入、支出只能填一项！")
            return
        if not money_in and not money_out:
            self.status_insert.set("收入、支出至少填一项！")
            return        # 默认视为 0 收入，你也可以改为 money_out = 0.0
        # raw_in  = self.money_in.get().strip()
        # raw_out = self.money_out.get().strip()

        # # 1. 两项都为空 → 必填
        # if not raw_in and not raw_out:
        #     self.status_insert.set("收入或支出必须填写一项！")
        #     return

        # # 2. 两项都有 → 冲突
        # if raw_in and raw_out:
        #     self.status_insert.set("收入、支出只能填一项！")
        #     return

        # try:
        #     if raw_in:
        #         money_in  = Decimal(raw_in)
        #         money_out = None
        #         if money_in <= 0:
        #             self.status_insert.set("收入必须为正数！")
        #             return
        #     else:               # raw_out 已保证非空
        #         money_out = Decimal(raw_out)
        #         money_in  = None
        #         if money_out <= 0:
        #             self.status_insert.set("支出必须为正数！")
        #             return
        # except InvalidOperation:
        #     self.status_insert.set("金额必须是合法数字！")
        
        # ---------- 日期 ----------
        date_str = self.date.get().strip()
        if not date_str:
            date_str = current_date           # 全局变量
        else:
            try:
                date_str = datetime.strptime(date_str, "%Y.%m.%d").strftime("%Y.%m.%d")
            except ValueError:
                self.status_insert.set("日期格式错误，请输入 YYYY.MM.DD")
                return

        # ---------- 生成下一条 ID ----------
        new_id = mysql_student.get_max_id() + 1
        record = (new_id, name, type_, source, money_in, money_out, date_str)

        # ---------- 插入数据库 ----------
        try:
            mysql_student.insert(record)
            self.status_insert.set("录入成功")  
            self.status_label.after(3000, lambda: self.status_insert.set(""))   # 3 秒后清除
           # self.clear_inputs()   # 可选：清空输入框
        except Exception as e:
            self.status_insert.set(f"录入失败：{e}")
            self.status_label.after(20000, lambda: self.status_insert.set(""))  # 20 秒后清除 

def fmt_money(val):
    """把 Decimal/int/float 转成无多余 0 的字符串"""
    if not val:          # 0 或 None
        return ''
    return f'{Decimal(val):.6f}'.rstrip('0').rstrip('.')  # 去掉多余 0 和可能残留的 .
class SearchFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.status_name = StringVar()
        self.status_out=StringVar()
        self.status_all=StringVar()
        self.table_search_view = Frame()

        self.show_table_search()

    # 实现显示查询页面的整个大框架分布
    def show_table_search(self):
        columns = ("id", "name", "type", "source", "money_in","money_out" ,"date")
        columns_values = ("序号", "姓名", "分类", "公司", "收入金额","支出金额" ,"日期")
        self.tree_view = ttk.Treeview(self, show = 'headings', columns = columns)


        for col in columns:
            self.tree_view.column(col, width = 10, anchor = 'center')

        for col, colvalue in zip(columns, columns_values):
            self.tree_view.heading(col, text = colvalue)

        self.tree_view.pack(fill = BOTH, expand = True)
        self.show_search_data()
        self.select_entry=StringVar()
        self.type_type = StringVar()
        self.name_entry = StringVar()
        self.name_source=StringVar()
        self.min_money_entry = StringVar()  # 添加最小金额输入框的变量
        self.max_money_entry = StringVar()  # 添加最大金额输入框的变量
        self.start_date_entry = StringVar()  # 添加开始日期输入框的变量
        self.end_date_entry = StringVar()  # 添加结束日期输入框的变量
        # Entry(self, textvariable=self.type_type,width=5).pack(side = LEFT)
        # Button(self, text='按类型查询', command=self.search_type).pack(side=LEFT) # , command = self.treeviewClick
        # Entry(self, textvariable=self.min_money_entry,width=5).pack(side=LEFT)
        # Entry(self, textvariable=self.max_money_entry,width=5).pack(side=LEFT)
        # Button(self, text = '删   除', command=self.treeviewClick).pack(side = RIGHT)
        # Button(self, text='按金额查询', command=self.search_money).pack(side=LEFT)
        # Entry(self, textvariable=self.start_date_entry,width=10).pack(side=LEFT)
        # Entry(self, textvariable=self.end_date_entry,width=10).pack(side=LEFT)
        # Button(self, text='按日期查询', command=self.search_date).pack(side=LEFT)
        # 综合查询输入框和按钮
        Label(self, text="选择模式：").pack(side=LEFT)
        Entry(self, textvariable=self.select_entry, width=5).pack(side=LEFT) 
        
        Label(self, text="分类：").pack(side=LEFT)
        Entry(self, textvariable=self.type_type, width=5).pack(side=LEFT)
         
        Label(self, text="姓名：").pack(side=LEFT)
        Entry(self, textvariable=self.name_entry, width=10).pack(side=LEFT) 
        Label(self, text="公司：").pack(side=LEFT)
        Entry(self, textvariable=self.name_source, width=10).pack(side=LEFT) 
       
        Label(self, text="金额范围：").pack(side=LEFT)
        Entry(self, textvariable=self.min_money_entry, width=5).pack(side=LEFT)
        Label(self, text="-").pack(side=LEFT)
        Entry(self, textvariable=self.max_money_entry, width=5).pack(side=LEFT)

        Label(self, text="日期范围：").pack(side=LEFT)
        Entry(self, textvariable=self.start_date_entry, width=10).pack(side=LEFT)
        Label(self, text="-").pack(side=LEFT)
        Entry(self, textvariable=self.end_date_entry, width=10).pack(side=LEFT)

        # 综合查询按钮
        Button(self, text='综合查询', command=self.search).pack(side=LEFT)

        # 删除按钮
        Button(self, text='删   除', command=self.treeviewClick).pack(side=RIGHT)

        Label(self, textvariable=self.status_name, fg="red").pack(side=TOP,pady=5)
        Label(self, textvariable=self.status_out, fg="green").pack(side=TOP, pady=5)
        Label(self, textvariable=self.status_all, fg="black").pack(side=TOP, pady=5)
        Button(self, text='导出Excel', command=self.export_to_excel).pack(side=RIGHT, padx=5)
          #点击标题实现排序
        # def treeview_sort_column1(tv, col, reverse):  # Treeview、列名、排列方式
        #     l = [(tv.set(k, col), k) for k in tv.get_children('')]
        #     if col == "date":  # 如果是日期列
        #         l.sort(key=lambda t: datetime.strptime(t[0], "%Y.%m.%d"), reverse=reverse)
        #     else:
        #         try:
        #          # 尝试将列值转换为整数（适用于数字列）
        #             l.sort(key=lambda t: int(t[0]), reverse=reverse)
        #         except ValueError:
        #     # 如果列值无法转换为整数（适用于字符串列），直接按字符串排序    
        #          l.sort(key=lambda t: t[0], reverse=reverse)
        #          l.sort(reverse=reverse)  # 排序方式
        #     for index, (val, k) in enumerate(l):  # 根据排序后索引移动
        #         tv.move(k, '', index)
        #     for index, (val, k) in enumerate(l):  # 根据排序后索引移动
        #         tv.move(k, '', index)
        #     tv.heading(col, command=lambda: treeview_sort_column1(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
        #     self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色
        from datetime import datetime

        def treeview_sort_column1(tv, col, reverse):  # Treeview、列名、排列方式
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == "date":  # 如果是日期列
                try:
                    l.sort(key=lambda t: datetime.strptime(t[0], "%Y.%m.%d"), reverse=reverse)
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                    l.sort(key=lambda t: t[0], reverse=reverse)  # 按字符串排序
            else:
                try:
                    # 尝试将列值转换为整数（适用于数字列）
                    l.sort(key=lambda t: Decimal(t[0].strip() or '0'), reverse=reverse)
                except ValueError:
                    # 如果列值无法转换为整数（适用于字符串列），直接按字符串排序
                    l.sort(key=lambda t: t[0], reverse=reverse)

            for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                tv.move(k, '', index)

            tv.heading(col, command=lambda: treeview_sort_column1(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
            # self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色


        def treeview_sort_column2(tv, col, reverse):  # Treeview、列名、排列方式
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == "date":  # 如果是日期列
                l.sort(key=lambda t: datetime.strptime(t[0], "%Y.%m.%d"), reverse=reverse)
            else:
                try:
                 # 尝试将列值转换为整数（适用于数字列）
                    l.sort(key=lambda t: Decimal(t[0].strip() or '0'), reverse=reverse)
                except ValueError:
            # 如果列值无法转换为整数（适用于字符串列），直接按字符串排序
                 l.sort(key=lambda t: t[0], reverse=reverse)
                 l.sort(reverse=reverse)  # 排序方式
            for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column2(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
            self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色

        for i in range(7):  # 给所有标题加（循环上边的“手工”）
            if i >= 1 and i <=2:
                self.tree_view.heading(columns[i], text=columns_values[i], command=lambda _col=columns[i]: treeview_sort_column2(self.tree_view, _col, False))
            else: self.tree_view.heading(columns[i], text = columns_values[i], command=lambda _col = columns[i]: treeview_sort_column1(self.tree_view, _col, False))
        # 定义背景色风格
        self.tree_view.tag_configure('even', background='lightblue')  # even标签设定为浅蓝色背景颜色

    def show_search_data(self):

        for _ in map(self.tree_view.delete, self.tree_view.get_children('')): # 删除原本显示的数据
            pass
        students = mysql_student.all() # 获取数据库中的信息并以字典形式返回
        index = -1
        total_money_in = 0
        total_money_out=0
        for stu in students:
            self.tree_view.insert('', index + 1, values=(
                    stu['id'], stu['name'], stu['type'], stu['source'],
                        fmt_money(stu['money_in']),
                    fmt_money(stu['money_out']) , stu['date']
                ))
            # 累加金额（只有当金额字段存在且为数字时）
            if 'money_in' in stu and isinstance(stu['money_in'], (int, Decimal)):
                total_money_in += stu['money_in']
            if 'money_out' in stu and isinstance(stu['money_out'], (int, Decimal)):
                total_money_out += stu['money_out']
        self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色
        self.status_name.set(f"收入：{fmt_money (total_money_in)}") 
        self.status_out.set(f"支出：{fmt_money(total_money_out)}") 
        self.status_all.set(f"综合：{fmt_money(total_money_in-total_money_out)}") 


    def tree_color(self):  # 表格栏隔行显示不同颜色函数
        items = self.tree_view.get_children()  # 得到根目录所有行的iid
        i = 0  # 初值
        for hiid in items:
            if i / 2 != int(i / 2):  # 判断奇偶
                tag1 = ''  # 奇数行
            else:
                tag1 = 'even'  # 偶数行
            self.tree_view.item(hiid, tag=tag1)  # 偶数行设为浅蓝色的tag='even'
            i += 1  # 累加1
    

 
    # def search(self):
    #     # 清空树形视图中的所有内容
    #     for item in self.tree_view.get_children():
    #         self.tree_view.delete(item)

    #     # 获取用户输入的查询条件
    #     select_entry=select_entry.get()
    #     type_name=self.name_entry.get()
    #     type_value = self.type_type.get()
    #     min_money = self.min_money_entry.get()
    #     max_money = self.max_money_entry.get()
    #     start_date = self.start_date_entry.get()
    #     end_date = self.end_date_entry.get()

    #     # 格式化日期输入
    #     try:
    #         if start_date:
    #             start_date = datetime.strptime(start_date, "%Y.%m.%d").strftime("%Y.%m.%d")
    #         if end_date:
    #             end_date = datetime.strptime(end_date, "%Y.%m.%d").strftime("%Y.%m.%d")
    #     except ValueError:
    #         self.status_name.set("请输入有效的日期格式（如 2021.01.01）")
    #         return

    #     # 检查输入的金额范围和日期范围是否合理
    #     if min_money and max_money:
    #         try:
    #             min_money =Decimal(min_money)
    #             max_money = Decimal(max_money)
    #             if min_money > max_money:
    #                 self.status_name.set("最小金额应小于最大金额")
    #                 return
    #         except ValueError:
    #             self.status_name.set("请输入有效的金额范围")
    #             return

    #     if start_date and end_date and start_date > end_date:
    #         self.status_name.set("开始日期应早于或等于结束日期")
    #         return

    #     # 调用数据库查询方法，根据综合条件搜索学生信息
    #     students = mysql_student.search(
    #         type_name=type_name if type_name else None,
    #         type_value=type_value if type_value else None,
    #         min_money=min_money if min_money else 0,
    #         max_money=max_money if max_money else 99999999999999999,
    #         start_date=start_date if start_date else min_date,
    #         end_date=end_date if end_date else current_date
    #     )

       
    #     total_money=0
    #     # 如果没有找到匹配的学生信息，提示用户
    #     if not students:
    #         self.status_name.set("总金额:0")
    #         return

    #     # 将搜索结果显示在树形视图中
    #     for stu in students:
    #         # 使用索引访问 tuple 中的字段
    #         id = stu[0] if len(stu) > 0 else 'N/A'
    #         name = stu[1] if len(stu) > 1 else 'N/A'
    #         type = stu[2] if len(stu) > 2 else 'N/A'
    #         source = stu[3] if len(stu) > 3 else 'N/A'
    #         money_in = stu[4] if len(stu) > 4 else 'N/A'
    #         money_out=stu[5] if len(stu) > 5 else 'N/A'
    #         date = stu[6] if len(stu) > 6 else 'N/A'

    #         self.tree_view.insert('', 'end', values=(id, name, type, source, money_in,money_out, date))
    #         # if money != 'N/A':
    #         #     try:
    #         #         total_money += decimal(money)  # 确保 money 是整数
    #         #     except ValueError:
    #         #         print(f"Warning: Invalid money value '{money}' for student {name}")
    #           # 只要 money_in / money_out 是数字就累加它们的和
    #         try:
    #             money_in  = Decimal(money_in)  if str(money_in).strip()  else 0
    #             money_out = Decimal(money_out) if str(money_out).strip() else 0
    #             total_money += money_in + money_out
    #         except ValueError:
    #             print(f"Warning: Invalid money_in or money_out for student {name}")


    #     # 设置树形视图的行背景颜色
    #     self.tree_color()
    #     self.status_name.set(f"总金额：{total_money}")
    def search(self):
        # 1. 清空表格
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        # 2. 读取界面输入
        mode_str       = self.select_entry.get()          # 0全部 1收入 -1支出
        mode_str = self.select_entry.get().strip()
        try:
            mode = int(mode_str)
        except ValueError:
            mode = 0  # 如果输入非法，默认显示全部mode_str = self.select_entry.get().strip()
        try:
            mode = int(mode_str)
        except ValueError:
               mode = 0  # 如果输入非法，默认显示全部
        type_value = self.type_type.get().strip()
        name_key   = self.name_entry.get().strip()
        source_key = self.name_source.get().strip()
        min_money  = self.min_money_entry.get().strip()
        max_money  = self.max_money_entry.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date   = self.end_date_entry.get().strip()

        # 3. 日期格式校验
        try:
            start_date = datetime.strptime(start_date, "%Y.%m.%d").strftime("%Y.%m.%d") if start_date else None
            end_date   = datetime.strptime(end_date,   "%Y.%m.%d").strftime("%Y.%m.%d") if end_date else None
        except ValueError:
            self.status_name.set("日期格式错误（YYYY.MM.DD）")
            return

        # 4. 金额范围校验
        try:
            min_money = Decimal(min_money) if min_money else Decimal('0')
            max_money = Decimal(max_money) if max_money else Decimal('99999999999.99999')
            if min_money > max_money:
                self.status_name.set("最小金额应≤最大金额")
                return
        except:
            self.status_name.set("金额必须为数字")
            return

        # 5. 调用数据库查询
        students = mysql_student.search(
            mode       = mode,
            name_key   = name_key or None,
            source_key=source_key or None,
            type_value = type_value or None,
            min_money  = min_money,
            max_money  = max_money,
            start_date = start_date,
            end_date   = end_date
        )

        # 6. 展示结果
        total_money_in = Decimal('0')
        total_money_out = Decimal('0')
        # if not students:
        #     self.status_name.set("总金额：0")
        #     return

        for stu in students:
            id, name, type_, source, money_in, money_out, date = stu
            if money_in and isinstance(money_in, (int, Decimal)):
                total_money_in += Decimal(money_in)
            if money_out and isinstance(money_out, (int, Decimal)):
                total_money_out += Decimal(money_out)
            self.tree_view.insert('', 'end',
                                values=(id, name, type_, source, fmt_money(money_in), fmt_money(money_out), date))

        self.tree_color()
      #  self.status_name.set(f"总金额：{total}")
        self.status_name.set(f"收入：{fmt_money(total_money_in)}")
        self.status_out.set(f"支出：{fmt_money(total_money_out)}")
        self.status_all.set(f"综合：{fmt_money(total_money_in - total_money_out)}")
            
    def treeviewClick(self):  # 单击
        for item in self.tree_view.selection():
            item_text = self.tree_view.item(item, "values")
            mysql_student.delete_id(item_text[0])  # 删除所选行的第一列的值
            self.show_search_data()

    def export_to_excel(self):
        # 获取当前树形视图中的所有数据
        items = self.tree_view.get_children()
        data = []
        columns = ("id", "name", "type", "source", "money_in","money_out", "date")  # 与Treeview列名对应
        
        for item in items:
            values = self.tree_view.item(item, 'values')
            data.append(values)
        
        if not data:
            messagebox.showwarning("警告", "没有数据可导出")
            return
        
        # 创建DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # 让用户选择保存位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="保存为Excel文件"
        )
        
        if not file_path:  # 用户取消了保存
            return
        
        try:
            # 导出到Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("成功", f"数据已成功导出到:\n{file_path}")
            import os
            os.startfile(os.path.dirname(file_path))
        except Exception as e:
            messagebox.showerror("错误", f"导出失败:\n{str(e)}")
        
 

class ChangeFrame(Frame):
    def __init__(self, root):
        super().__init__(root, width=570, height=290)
        #super().__init__(root)  # 移除 width 和 height
        #self.pack(fill=BOTH, expand=True)  # 自适应父容器
        self.pack()

        self.change_student = StringVar()
        self.status_student = StringVar()
        self.status_name = StringVar()

        # 存储学生信息的变量
        self.id = StringVar()
        self.name = StringVar()
        self.kulas = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.english_out=StringVar()
        self.computer = StringVar()

        self.insert_page()

    def insert_page(self):
        Label(self, text='请输入需要查询人员的').place(x=40, y=60)
        Label(self, text='姓名或者序号').place(x=64, y=80)
        Entry(self, textvariable=self.change_student).place(x=30, y=100)
        Button(self, text='按序号查询', command=self.id_change).place(x=30, y=130)
        Button(self, text='按姓名查询', command=self.name_change).place(x=110, y=130)
        Label(self, textvariable=self.status_student).place(x=45, y=160)

        Label(self, text='序   号 : ').place(x=240, y=20)
        Entry(self, textvariable=self.id, state="readonly").place(x=320, y=20)

        Label(self, text='姓   名 : ').place(x=240, y=50)
        Entry(self, textvariable=self.name).place(x=320, y=50)

        Label(self, text='分   类 : ').place(x=240, y=80)
        Entry(self, textvariable=self.kulas).place(x=320, y=80)

        Label(self, text='来   源 : ').place(x=240, y=110)
        Entry(self, textvariable=self.math).place(x=320, y=110)

        Label(self, text='收 入 金 额 : ').place(x=240, y=140)
        Entry(self, textvariable=self.english).place(x=320, y=140)

        Label(self, text='支 出 金 额 : ').place(x=240, y=170)
        Entry(self, textvariable=self.english_out).place(x=320, y=170)

        Label(self, text='日   期 : ').place(x=240, y=200)
        Entry(self, textvariable=self.computer).place(x=320, y=200)

        Button(self, text='修    改', command=self.update_student_info).place(x=320, y=250)
        Button(self, text='删    除', command=self.delete_student).place(x=400, y=250)
        Label(self, textvariable=self.status_name,fg='red').place(x=0, y=170)

        # 新增 Listbox 控件用于显示查询到的多个同名学生信息
        self.listbox = Listbox(self, width=30, height=5)
        self.listbox.place(x=30, y=190)
        self.listbox.bind('<<ListboxSelect>>', self.show_selected_student)  # 绑定选择事件

    def id_change(self):
        student_id = self.change_student.get()
        if student_id:
            flag, result = mysql_student.search_id(student_id)
            if flag:
                self.show_student_details(result[0])
                self.status_student.set("查询成功")
            else:
                self.status_student.set(result)
        else:
            self.status_student.set("请输入学号")

    def name_change(self):
        student_name = self.change_student.get()
        if student_name:
            flag, result = mysql_student.search_name(student_name)
            if flag:
                self.update_listbox(result)
                self.status_student.set("查询到以下人员，请选择")
                # 默认显示第一个学生的信息
                if result:
                    self.show_student_details(result[0])
            else:
                self.status_student.set(result)
        else:
            self.status_student.set("请输入姓名")

    def update_listbox(self, students):
        self.listbox.delete(0, END)  # 清空 Listbox
        for stu in students:
            self.listbox.insert(END, f"学号: {stu[0]}, 姓名: {stu[1]}")

    def show_selected_student(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            data = self.listbox.get(index)
            selected_id = data.split(",")[0].split(":")[1].strip()
            flag, result = mysql_student.search_id(selected_id)
            if flag:
                self.show_student_details(result[0])
            else:
                self.status_student.set("无法获取详细人员信息")
        else:
            self.status_student.set("未选择人员")

    def show_student_details(self, student):
        self.id.set(student[0])
        self.name.set(student[1])
        self.kulas.set(student[2])
        self.math.set(student[3])
        self.english.set(student[4])
        self.english_out.set(student[5])
        self.computer.set(student[6])

    def update_student_info(self):
        student_id = self.id.get()
        if not student_id:
            self.status_name.set("未选择人员或id为空")
            return

        new_data = (
            self.name.get(),
            self.kulas.get(),
            self.math.get(),
            self.english.get(),
            self.english_out.get(),
            self.computer.get()
        )

        flag, msg = mysql_student.update_student(student_id, new_data)
        if flag:
            self.status_name.set(msg)
            self.after(5000, lambda: self.status_name.set(""))  # 20 秒后清除
            # 更新 Listbox 内容
            self.update_listbox(mysql_student.search_name(self.change_student.get())[1])
        else:
            self.status_name.set(f"更新失败：{msg}")
            self.after(5000, lambda: self.status_name.set(""))  # 20 秒后清除 

    def delete_student(self):
        student_id = self.id.get()
        if not student_id:
            self.status_name.set("未选择人员或id为空")
            return

        flag, msg = mysql_student.delete_id(student_id)
        if flag:
            self.status_name.set(msg)
            self.after(5000, lambda: self.status_name.set(""))  # 20 秒后清除
            # 更新 Listbox 内容
            self.update_listbox(mysql_student.search_name(self.change_student.get())[1])
            self.clear_details()
        else:
            self.status_name.set(f"删除失败：{msg}")
            self.after(5000, lambda: self.status_name.set(""))  # 20 秒后清除

    def clear_details(self):
        self.id.set("")
        self.name.set("")
        self.kulas.set("")
        self.math.set("")
        self.english.set("")
        self.english_out.set("")
        self.computer.set("")

 
      
# 实现帮助页面的类，主要打印一些程序运行的帮助以及规则
class HelpFrame(Frame):
    def __init__(self, root):
        super().__init__(root)

        Label(self, text = '关于录入界面').pack()
        Label(self, text = '序号是默认输入的，不需要手动输入，并且日期如果没填入默认是当前日期').pack()
        Label(self, text = ' ').pack()
        Label(self, text = '关于查询界面').pack()
        Label(self, text = '默认为升序排列，可以根据员工的各类信息进行排列，点击小标题可去实现升序和降序').pack()
        Label(self, text = '可以查看数据信息以及可以选择信息进行删除').pack()
        Label(self, text = ' ').pack()
        Label(self, text = '关于删除界面').pack()
        Label(self, text = '可以根据序号或者姓名对员工1信息进行删除，序号是唯一的').pack()
        Label(self, text = ' ').pack()
        Label(self, text = '关于修改界面').pack()
        Label(self, text = '可以通过序号或者姓名来查询员工信息，一定序号不能手动修改！！！但查询名字只会出现第一位员工，按下修改键出现提示即成功').pack()
 