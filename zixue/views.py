from tkinter import *
from tkinter import ttk
import mysql_student
from tkinter import messagebox
import pandas as pd
from tkcalendar import DateEntry 
from tkinter import filedialog, messagebox
from datetime import datetime  # 导入 datetime 模块
import re
from decimal import Decimal
from decimal import Decimal, InvalidOperation
current_date = datetime.now().strftime("%Y.%m.%d")
allminmoney_in=mysql_student.get_min_money()
allmaxmoney=mysql_student.get_max_money()
min_date=mysql_student.get_min_date()
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
        self.grid(sticky="nsew")
        self.id = StringVar()
        self.name = StringVar()
        self.type = StringVar()
        self.source = StringVar()
        self.money_in = StringVar()
        self.money_out = StringVar()
        self.date = StringVar()
        self.date.set(current_date)
        self.status_insert = StringVar()
        # 在 InsertFrame 的 __init__ 方法中添加
        self.type_options = [
            "1: 纱运费",
            "2: 纱款",
            "3: 下角料",
            "4: 工资",
            "5: 配件",
            "6: 棉花款",
            "7: 电费",
            "8: 税收",
            "9: 其他"
        ]
        self.insert_page()

    def insert_page(self):
        # 配置行和列的权重，使控件可拉伸
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

        # 标签和输入框
        Label(self, text='姓   名 : ').grid(row=2, column=1, pady=5, sticky="e")
        self.entry_name = Entry(self, textvariable=self.name)
        self.entry_name.grid(row=2, column=2, pady=5, sticky="ew")

        # Label(self, text='类 别 : ').grid(row=3, column=1, pady=5, sticky="e")
        # self.entry_type = Entry(self, textvariable=self.type)
        # self.entry_type.grid(row=3, column=2, pady=5, sticky="ew")
        Label(self, text='类 别 : ').grid(row=3, column=1, pady=5, sticky="e")

        # 创建 Combobox
        self.entry_type = ttk.Combobox(self, textvariable=self.type, values=self.type_options, state="readonly")
        self.entry_type.grid(row=3, column=2, pady=5, sticky="ew")

        # 设置默认值（可选）
        self.entry_type.set("请选择类别")

        Label(self, text='公 司 : ').grid(row=4, column=1, pady=5, sticky="e")
        self.entry_source = Entry(self, textvariable=self.source)
        self.entry_source.grid(row=4, column=2, pady=5, sticky="ew")

        Label(self, text='收 入 金 额 : ').grid(row=5, column=1, pady=5, sticky="e")
        self.entry_money_in = ThousandsEntry(self, textvariable=self.money_in)
        self.entry_money_in.grid(row=5, column=2, pady=5, sticky="ew")

        Label(self, text='支 出 金 额 : ').grid(row=6, column=1, pady=5, sticky="e")
        self.entry_money_out = ThousandsEntry(self, textvariable=self.money_out)
        self.entry_money_out.grid(row=6, column=2, pady=5, sticky="ew")

        Label(self, text='日 期 : ').grid(row=7, column=1, pady=5, sticky="e")
        self.entry_date = DateEntry(self, textvariable=self.date, date_pattern='yyyy.mm.dd')
        self.entry_date.grid(row=7, column=2, pady=5, sticky="ew")

        Button(self, text='清空', command=self.insert_deleteValue).grid(row=8, column=1, pady=10, sticky="e")
        Button(self, text='录入', command=self.insert_data).grid(row=8, column=3, pady=10, sticky="w")

        self.status_label = Label(self, textvariable=self.status_insert, fg='red')
        self.status_label.grid(row=9, column=2, padx=10, sticky="ew")
    def insert_deleteValue(self):
        #self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_type.delete(0, END)
        self.entry_source.delete(0, END)
        self.entry_money_in.delete(0, END)
        self.entry_money_out.delete(0, END)
        self.entry_date.delete(0, END)

    def insert_data(self):
        # ---------- 基础字段 ----------
        name   = self.name.get().strip()   or 'NULL'
        type_  = self.type.get().strip()   or 'NULL'
        source = self.source.get().strip() or 'NULL'

       # ---------- 金额：只能填 money_in 或 money_out 中的一项 ----------
        try:    
            money_in = self.entry_money_in.get_number()
            money_out = self.entry_money_out.get_number()

            # 转换为 Decimal
            money_in = Decimal(str(money_in))
            money_out = Decimal(str(money_out))
        except ValueError:
            self.status_insert.set("金额必须是数字！")  
            self.status_label.after(5000, lambda: self.status_insert.set(""))  # 20 秒后清除
            return

        # 业务校验：二者只能有一个大于 0
        if money_in and money_out:
            self.status_insert.set("收入、支出只能填一项！")
            self.status_label.after(5000, lambda: self.status_insert.set(""))  # 20 秒后清除
            return
        if not money_in and not money_out:
            self.status_insert.set("收入、支出至少填一项！")
            self.status_label.after(5000, lambda: self.status_insert.set(""))  # 20 秒后清除
            return

        # ---------- 日期 ----------
        # 从 DateEntry 获取日期
        try:
            date_obj = self.entry_date.get_date()  # 获取日期对象
            date_str = date_obj.strftime("%Y.%m.%d")  # 转换为字符串格式
        except Exception:
            # 如果出现问题，使用当前日期作为备选
            date_str = current_date
        # ---------- 检查重复数据 ----------
        duplicate_count = mysql_student.check_duplicate(name, type_, source, money_in, money_out, date_str)
       
        if duplicate_count > 0:
            # 弹出确认对话框询问用户是否继续录入
            result = messagebox.askyesno(
                "重复数据警告", 
                f"数据库中已存在 {duplicate_count} 条相同记录，是否仍要录入？"
            )
            if not result:
                self.status_insert.set("录入已取消")
                self.status_label.after(3000, lambda: self.status_insert.set(""))
                return

        # ---------- 生成下一条 ID ----------
        new_id = mysql_student.get_max_id() + 1
        record = (new_id, name, type_, source, money_in, money_out, date_str)

        # ---------- 插入数据库 ----------
        try:
            mysql_student.insert(record)
            self.status_insert.set("录入成功")  
            self.status_label.after(3000, lambda: self.status_insert.set(""))   # 3 秒后清除
        except Exception as e:
            self.status_insert.set(f"录入失败：{e}")
            self.status_label.after(10000, lambda: self.status_insert.set(""))  # 20 秒后清除 
def fmt_money(val):
    """把 Decimal/int/float 转成无多余 0 的字符串"""
    if not val:          # 0 或 None
        return ''
    return f'{Decimal(val):.6f}'.rstrip('0').rstrip('.')  # 去掉多余 0 和可能残留的 .
# views.py
class SearchFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(sticky="nsew")
        # 确保配置了 grid 权重
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.status_name = StringVar()
        self.status_out = StringVar()
        self.status_all = StringVar()
        self.table_search_view = Frame()

        self.select_entry = StringVar()
        self.type_type = StringVar()
        self.name_entry = StringVar()
        self.name_source = StringVar()
        self.min_money_entry = StringVar()
        self.max_money_entry = StringVar()
        self.start_date_entry = StringVar()
        self.end_date_entry = StringVar()
       
        self.type_options = [
            "1: 纱运费",
            "2: 纱款",
            "3: 下角料",
            "4: 工资",
            "5: 配件",
            "6: 棉花款",
            "7: 电费",
            "8: 税收",
            "9: 其他"
        ]
        # 用于自动补全的列表
        self.name_list = []
        self.source_list = []

        # 用于自动补全的列表框
        self.name_listbox = None
        self.source_listbox = None

        # 配置 Treeview 样式
        self.configure_treeview_style()

        self.show_table_search()

    def configure_treeview_style(self):
        """配置 Treeview 的样式，包括字体大小"""
        style = ttk.Style()
        # 设置 Treeview 的字体大小
        style.configure("Treeview", font=("Arial", 12), rowheight=30)
        # 设置表头的字体大小
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    def show_table_search(self):
        columns = ("id", "name", "type", "source", "money_in", "money_out", "date")
        columns_values = ("序号", "姓名", "分类", "公司", "收入金额", "支出金额", "日期")
        self.tree_view = ttk.Treeview(self, show='headings', columns=columns)

        for col in columns:
            self.tree_view.column(col, width=10, anchor='center')

        for col, colvalue in zip(columns, columns_values):
            self.tree_view.heading(col, text=colvalue)

        # Treeview 占据大部分空间
        self.tree_view.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # 配置网格权重
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # 输入区域
        input_frame = Frame(self)
        input_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        # 配置input_frame的列权重
        for i in range(10):
            input_frame.grid_columnconfigure(i, weight=1)

        # 创建日期输入框架
        date_frame = Frame(input_frame)
        date_frame.grid(row=0, column=0, columnspan=10, sticky="ew", pady=5)

        # 查询条件输入
        # Label(input_frame, text="选择模式：").grid(row=1, column=0, padx=5, sticky="w")
        # Entry(input_frame, textvariable=self.select_entry, width=5).grid(row=1, column=1, padx=5, sticky="w")
        
        # Label(input_frame, text="分类：").grid(row=1, column=2, padx=5, sticky="w")
        # Entry(input_frame, textvariable=self.type_type, width=10).grid(row=1, column=3, padx=5, sticky="w")
        
        # Label(input_frame, text="姓名：").grid(row=1, column=4, padx=5, sticky="w")
        # self.name_entry_widget = Entry(input_frame, textvariable=self.name_entry, width=10)
        # self.name_entry_widget.grid(row=1, column=5, padx=5, sticky="w")
        
        # Label(input_frame, text="公司：").grid(row=1, column=6, padx=5, sticky="w")
        # self.name_source_widget = Entry(input_frame, textvariable=self.name_source, width=10)
        # self.name_source_widget.grid(row=1, column=7, padx=5, sticky="w")
        # 统一设置 padding 和 width
        Label(input_frame, text="选择模式：").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        Entry(input_frame, textvariable=self.select_entry, width=6).grid(row=1, column=1, padx=5, pady=5, sticky="w")

       # 替换为以下代码
        Label(input_frame, text="分类：").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.type_type_combobox = ttk.Combobox(input_frame, textvariable=self.type_type, values=self.type_options, width=10, state="readonly")
        self.type_type_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.type_type_combobox.set("")  # 默认为空，表示不筛选

        # Label(input_frame, text="姓名：").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        # Entry(input_frame, textvariable=self.name_entry, width=10).grid(row=1, column=5, padx=5, pady=5, sticky="w")

        # Label(input_frame, text="公司：").grid(row=1, column=6, padx=5, pady=5, sticky="w")
        # Entry(input_frame, textvariable=self.name_source, width=10).grid(row=1, column=7, padx=5, pady=5, sticky="w")   

        # 姓名输入框
        Label(input_frame, text="姓名：").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.name_entry_widget = Entry(input_frame, textvariable=self.name_entry, width=10)
        self.name_entry_widget.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        # 公司输入框
        Label(input_frame, text="公司：").grid(row=1, column=6, padx=5, pady=5, sticky="w")
        self.name_source_widget = Entry(input_frame, textvariable=self.name_source, width=10)
        self.name_source_widget.grid(row=1, column=7, padx=5, pady=5, sticky="w")        

        
        Label(input_frame, text="金额范围：").grid(row=2, column=0, padx=5, sticky="w")
        Entry(input_frame, textvariable=self.min_money_entry, width=10).grid(row=2, column=1, padx=5, sticky="w")
        Label(input_frame, text="-").grid(row=2, column=2, padx=5, sticky="w")
        Entry(input_frame, textvariable=self.max_money_entry, width=10).grid(row=2, column=3, padx=5, sticky="w")

        Label(input_frame, text="日期范围：").grid(row=3, column=0, padx=5, sticky="w")
        
        # # 开始日期选择器
        # Label(date_frame, text="从:").grid(row=0, column=0, padx=5, sticky="w")
        # self.start_date_calendar = DateEntry(date_frame, textvariable=self.start_date_entry, 
        #                                 date_pattern='yyyy.mm.dd', width=12)
        # self.start_date_calendar.grid(row=0, column=1, padx=5, sticky="w")
        
        # # 结束日期选择器
        # Label(date_frame, text="到:").grid(row=0, column=2, padx=5, sticky="w")
        # self.end_date_calendar = DateEntry(date_frame, textvariable=self.end_date_entry, 
        #                                 date_pattern='yyyy.mm.dd', width=12)
        # self.end_date_calendar.grid(row=0, column=3, padx=5, sticky="w")
        # 开始日期选择器
        Label(date_frame, text="从:").grid(row=0, column=0, padx=5, sticky="w")
        self.start_date_calendar = DateEntry(date_frame, textvariable=self.start_date_entry, 
                                        date_pattern='yyyy.mm.dd', width=12)
        self.start_date_calendar.grid(row=0, column=1, padx=5, sticky="w")

        # 结束日期选择器
        Label(date_frame, text="到:").grid(row=0, column=2, padx=5, sticky="w")
        self.end_date_calendar = DateEntry(date_frame, textvariable=self.end_date_entry, 
                                        date_pattern='yyyy.mm.dd', width=12)
        self.end_date_calendar.grid(row=0, column=3, padx=5, sticky="w")
        # # 综合查询按钮
        # Button(input_frame, text='综合查询', command=self.search).grid(row=3, column=4, padx=5, pady=5, sticky="w")

        # # 删除按钮
        # Button(input_frame, text='删   除', command=self.treeviewClick).grid(row=3, column=5, padx=5, pady=5, sticky="w")
        button_frame = Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=8, padx=5, pady=5, sticky="ew")

        Button(button_frame, text='综合查询', command=self.search).pack(side=LEFT, padx=5)
        Button(button_frame, text='删   除', command=self.treeviewClick).pack(side=LEFT, padx=5)
        Button(button_frame, text='导出Excel', command=self.export_to_excel).pack(side=LEFT, padx=5)
        # 状态标签
        status_frame = Frame(self)
        status_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        Label(status_frame, textvariable=self.status_name, fg="red").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        Label(status_frame, textvariable=self.status_out, fg="green").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        Label(status_frame, textvariable=self.status_all, fg="black").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # 导出Excel按钮
        # Button(status_frame, text='导出Excel', command=self.export_to_excel).grid(row=0, column=3, padx=5, pady=5, sticky="e")

        # 绑定输入事件以实现自动补全
        self.name_entry.trace('w', self.update_name_suggestions)
        self.name_source.trace('w', self.update_source_suggestions)

        # 初始化数据
        self.show_search_data()

        # 设置排序功能
        from datetime import datetime

        def treeview_sort_column1(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == "date":
                try:
                    l.sort(key=lambda t: datetime.strptime(t[0], "%Y.%m.%d"), reverse=reverse)
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                    l.sort(key=lambda t: t[0], reverse=reverse)
            else:
                try:
                    l.sort(key=lambda t: Decimal(t[0].strip() or '0'), reverse=reverse)
                except ValueError:
                    l.sort(key=lambda t: t[0], reverse=reverse)

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            tv.heading(col, command=lambda: treeview_sort_column1(tv, col, not reverse))

        def treeview_sort_column2(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == "date":
                l.sort(key=lambda t: datetime.strptime(t[0], "%Y.%m.%d"), reverse=reverse)
            else:
                try:
                    l.sort(key=lambda t: Decimal(t[0].strip() or '0'), reverse=reverse)
                except ValueError:
                    l.sort(key=lambda t: t[0], reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column2(tv, col, not reverse))
            self.tree_color()

        for i in range(7):
            if i >= 1 and i <= 2:
                self.tree_view.heading(columns[i], text=columns_values[i], command=lambda _col=columns[i]: treeview_sort_column2(self.tree_view, _col, False))
            else:
                self.tree_view.heading(columns[i], text=columns_values[i], command=lambda _col=columns[i]: treeview_sort_column1(self.tree_view, _col, False))

        # 定义背景色风格
        self.tree_view.tag_configure('even', background='lightblue')
    def show_search_data(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        students = mysql_student.all()
        index = -1
        total_money_in = 0
        total_money_out = 0

        # 更新自动补全列表
        self.name_list = list(set([stu['name'] for stu in students if stu['name'] != 'NULL']))
        self.source_list = list(set([stu['source'] for stu in students if stu['source'] != 'NULL']))

        for stu in students:
            self.tree_view.insert('', index + 1, values=(
                stu['id'], stu['name'], stu['type'], stu['source'],
                fmt_money(stu['money_in']),
                fmt_money(stu['money_out']), stu['date']
            ))
            if 'money_in' in stu and isinstance(stu['money_in'], (int, Decimal)):
                total_money_in += stu['money_in']
            if 'money_out' in stu and isinstance(stu['money_out'], (int, Decimal)):
                total_money_out += stu['money_out']
        self.tree_color()
        self.status_name.set(f"收入：{fmt_money(total_money_in)}")
        self.status_out.set(f"支出：{fmt_money(total_money_out)}")
        self.status_all.set(f"综合：{fmt_money(total_money_in - total_money_out)}")

    # 其他方法保持不变...
    def update_name_suggestions(self, *args):
        """更新姓名自动补全建议"""
        self.update_suggestions(self.name_entry_widget, self.name_list, "name")
        
    def update_source_suggestions(self, *args):
        """更新公司自动补全建议"""
        self.update_suggestions(self.name_source_widget, self.source_list, "source")
        
    def update_suggestions(self, entry_widget, suggestion_list, list_type):
        """通用的更新建议函数"""
        # 销毁现有的建议列表框
        if list_type == "name" and self.name_listbox:
            self.name_listbox.destroy()
            self.name_listbox = None
        elif list_type == "source" and self.source_listbox:
            self.source_listbox.destroy()
            self.source_listbox = None
            
        value = entry_widget.get().strip()
        
        if not value:
            return
            
        # 获取匹配的建议
        suggestions = [item for item in suggestion_list if item.lower().startswith(value.lower())]
        
        if not suggestions:
            return
            
        # 创建建议列表框
        x = entry_widget.winfo_rootx() - self.winfo_rootx()
        y = entry_widget.winfo_rooty() - self.winfo_rooty() + entry_widget.winfo_height()
        
        if list_type == "name":
            self.name_listbox = Listbox(self, height=min(5, len(suggestions)), width=entry_widget.winfo_width())
            self.name_listbox.place(x=x, y=y)
            listbox = self.name_listbox
        else:
            self.source_listbox = Listbox(self, height=min(5, len(suggestions)), width=entry_widget.winfo_width())
            self.source_listbox.place(x=x, y=y)
            listbox = self.source_listbox
            
        for suggestion in suggestions:
            listbox.insert(END, suggestion)
            
        # 绑定事件
        listbox.bind("<ButtonRelease-1>", lambda e: self.select_suggestion(entry_widget, listbox, list_type))
        listbox.bind("<Escape>", lambda e: self.hide_suggestions(list_type))
        listbox.bind("<FocusOut>", lambda e: self.hide_suggestions(list_type))
        
        # 绑定Entry的事件
        entry_widget.bind("<Down>", lambda e: self.focus_listbox(listbox))
        entry_widget.bind("<Escape>", lambda e: self.hide_suggestions(list_type))
        
    def select_suggestion(self, entry_widget, listbox, list_type):
        """选择建议项"""
        if listbox.curselection():
            selection = listbox.get(listbox.curselection()[0])
            entry_widget.delete(0, END)
            entry_widget.insert(0, selection)
        self.hide_suggestions(list_type)
        entry_widget.focus_set()
        
    def focus_listbox(self, listbox):
        """将焦点转移到列表框"""
        if listbox.size() > 0:
            listbox.selection_set(0)
            listbox.focus_set()
            
    def hide_suggestions(self, list_type):
        """隐藏建议列表"""
        if list_type == "name" and self.name_listbox:
            self.name_listbox.destroy()
            self.name_listbox = None
        elif list_type == "source" and self.source_listbox:
            self.source_listbox.destroy()
            self.source_listbox = None
            
    def tree_color(self):
        items = self.tree_view.get_children()
        i = 0
        for hiid in items:
            if i / 2 != int(i / 2):
                tag1 = ''
            else:
                tag1 = 'even'
            self.tree_view.item(hiid, tag=tag1)
            i += 1

    def search(self):
        # 隐藏所有自动补全建议
        self.hide_suggestions("name")
        self.hide_suggestions("source")
        
        # 1. 清空表格
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        # 2. 读取界面输入
        mode_str = self.select_entry.get().strip()
        try:
            mode = int(mode_str)
        except ValueError:
            mode = 0
        type_value = self.type_type.get().strip()
        name_key = self.name_entry.get().strip()
        source_key = self.name_source.get().strip()
        min_money = self.min_money_entry.get().strip()
        max_money = self.max_money_entry.get().strip()
        
        # 从 DateEntry 控件获取日期值
        start_date = self.start_date_calendar.get() if self.start_date_calendar.get() else None
        end_date = self.end_date_calendar.get() if self.end_date_calendar.get() else None

        # 3. 日期格式校验
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y.%m.%d").strftime("%Y.%m.%d")
            except ValueError:
                self.status_name.set("开始日期格式错误")
                return
        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y.%m.%d").strftime("%Y.%m.%d")
            except ValueError:
                self.status_name.set("结束日期格式错误")
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
            mode=mode,
            name_key=name_key or None,
            source_key=source_key or None,
            type_value=type_value or None,
            min_money=min_money,
            max_money=max_money,
            start_date=start_date,
            end_date=end_date
        )

        # 6. 展示结果
        total_money_in = Decimal('0')
        total_money_out = Decimal('0')

        for stu in students:
            id, name, type_, source, money_in, money_out, date = stu
            if money_in and isinstance(money_in, (int, Decimal)):
                total_money_in += Decimal(money_in)
            if money_out and isinstance(money_out, (int, Decimal)):
                total_money_out += Decimal(money_out)
            self.tree_view.insert('', 'end',
                                values=(id, name, type_, source, fmt_money(money_in), fmt_money(money_out), date))

        self.tree_color()
        self.status_name.set(f"收入：{fmt_money(total_money_in)}")
        self.status_out.set(f"支出：{fmt_money(total_money_out)}")
        self.status_all.set(f"综合：{fmt_money(total_money_in - total_money_out)}")
        
    def treeviewClick(self):
        for item in self.tree_view.selection():
            item_text = self.tree_view.item(item, "values")
            mysql_student.delete_id(item_text[0])
            self.show_search_data()

    def export_to_excel(self):
        items = self.tree_view.get_children()
        data = []
        columns = ("id", "name", "type", "source", "money_in", "money_out", "date")
        
        for item in items:
            values = self.tree_view.item(item, 'values')
            data.append(values)
        
        if not data:
            messagebox.showwarning("警告", "没有数据可导出")
            return
        
        df = pd.DataFrame(data, columns=columns)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="保存为Excel文件"
        )
        
        if not file_path:
            return
        
        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("成功", f"数据已成功导出到:\n{file_path}")
            import os
            os.startfile(os.path.dirname(file_path))
        except Exception as e:
            messagebox.showerror("错误", f"导出失败:\n{str(e)}")

# # 在 views.py 中修改 ChangeFrame 类
# class ChangeFrame(Frame):
#     def __init__(self, root):
#         super().__init__(root)
#         # 移除 width 和 height 参数，让 Frame 可以自适应
#         self.grid(sticky="nsew")
        
#         # 配置行列权重以支持缩放
#         for i in range(15):
#             self.grid_rowconfigure(i, weight=1)
#         for j in range(4):
#             self.grid_columnconfigure(j, weight=1)

#         self.change_student = StringVar()
#         self.status_student = StringVar()
#         self.status_name = StringVar()

#         # 存储学生信息的变量
#         self.id = StringVar()
#         self.name = StringVar()
#         self.kulas = StringVar()
#         self.math = StringVar()
#         self.english = StringVar()
#         self.english_out = StringVar()
#         self.computer = StringVar()  # 这个变量用于存储日期
#         self.type_options = [
#             "1: 纱运费",
#             "2: 纱款",
#             "3: 下角料",
#             "4: 工资",
#             "5: 配件",
#             "6: 棉花款",
#             "7: 电费",
#             "8: 税收",
#             "9: 其他"
#         ]

#         self.insert_page()

#     def insert_page(self):
#         # 查询区域
#         query_frame = Frame(self)
#         query_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
#         Label(query_frame, text='请输入需要查询人员的姓名或者序号').grid(row=0, column=0, padx=5, pady=5, sticky="w")
#         # Label(query_frame, text='姓名或者序号').grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
#         Entry(query_frame, textvariable=self.change_student).grid(row=3, column=1, rowspan=2, padx=5, pady=5, sticky="ew")
#         Button(query_frame, text='按序号查询', command=self.id_change).grid(row=3, column=2, padx=5, pady=5, sticky="ew")
#         Button(query_frame, text='按姓名查询', command=self.name_change).grid(row=4, column=2, padx=5, pady=5, sticky="ew")
        
#         query_frame.grid_columnconfigure(1, weight=1)

#         Label(self, textvariable=self.status_student).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

#         # 信息显示和编辑区域
#         info_frame = Frame(self)
#         info_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
#         self.grid_rowconfigure(2, weight=1)

#         # 配置info_frame的行列
#         for i in range(8):
#             info_frame.grid_rowconfigure(i, weight=1)
#         for j in range(3):
#             info_frame.grid_columnconfigure(j, weight=1)

#         Label(info_frame, text='序   号 : ').grid(row=0, column=0, padx=5, pady=5, sticky="e")
#         Entry(info_frame, textvariable=self.id, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="ew")

#         Label(info_frame, text='姓   名 : ').grid(row=1, column=0, padx=5, pady=5, sticky="e")
#         Entry(info_frame, textvariable=self.name).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

#         Label(info_frame, text='分   类 : ').grid(row=2, column=0, padx=5, pady=5, sticky="e")
#         # Entry(info_frame, textvariable=self.kulas).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
#         self.kulas_combobox = ttk.Combobox(info_frame, textvariable=self.kulas, values=self.type_options, width=12, state="readonly")
#         self.kulas_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

#         Label(info_frame, text='来   源 : ').grid(row=3, column=0, padx=5, pady=5, sticky="e")
#         Entry(info_frame, textvariable=self.math).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

#         Label(info_frame, text='收 入 金 额 : ').grid(row=4, column=0, padx=5, pady=5, sticky="e")
#         Entry(info_frame, textvariable=self.english).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

#         Label(info_frame, text='支 出 金 额 : ').grid(row=5, column=0, padx=5, pady=5, sticky="e")
#         Entry(info_frame, textvariable=self.english_out).grid(row=5, column=1, padx=5, pady=5, sticky="ew")

#         Label(info_frame, text='日   期 : ').grid(row=6, column=0, padx=5, pady=5, sticky="e")
#         # 使用 DateEntry 替代原来的 Entry
#         self.computer_calendar = DateEntry(info_frame, textvariable=self.computer, date_pattern='yyyy.mm.dd', width=12)
#         self.computer_calendar.grid(row=6, column=1, padx=5, pady=5, sticky="w")

#         # 按钮区域
#         button_frame = Frame(self)
#         button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
#         Button(button_frame, text='修    改', command=self.update_student_info).pack(side=LEFT, padx=10)
#         Button(button_frame, text='删    除', command=self.delete_student).pack(side=LEFT, padx=10)
        
#         # 状态标签
#         Label(self, textvariable=self.status_name, fg='red').grid(row=4, column=0, columnspan=2, padx=5, pady=5)

#         # 新增 Listbox 控件用于显示查询到的多个同名学生信息
#         listbox_frame = Frame(self)
#         listbox_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="nsew")
#         self.grid_columnconfigure(2, weight=1)
#         self.grid_rowconfigure(3, weight=1)
        
#         Label(listbox_frame, text="查询结果:").pack(anchor=W)
#         self.listbox = Listbox(listbox_frame, width=30, height=10)
#         self.listbox.pack(fill=BOTH, expand=True, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.show_selected_student)  # 绑定选择事件# 在 views.py 中修改 ChangeFrame 类
class ChangeFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        # 移除 width 和 height 参数，让 Frame 可以自适应
        self.grid(sticky="nsew")
        
        # 配置行列权重以支持缩放
        for i in range(15):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

        self.change_student = StringVar()
        self.status_student = StringVar()
        self.status_name = StringVar()

        # 存储学生信息的变量
        self.id = StringVar()
        self.name = StringVar()
        self.kulas = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.english_out = StringVar()
        self.computer = StringVar()  # 这个变量用于存储日期
        self.type_options = [
            "1: 纱运费",
            "2: 纱款",
            "3: 下角料",
            "4: 工资",
            "5: 配件",
            "6: 棉花款",
            "7: 电费",
            "8: 税收",
            "9: 其他"
        ]

        self.insert_page()

    def insert_page(self):
        # 查询区域
        query_frame = Frame(self)
        query_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        Label(query_frame, text='请输入需要查询人员的').grid(row=0, column=0, padx=5, pady=5, sticky="w")
        Label(query_frame, text='姓名或者序号').grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        Entry(query_frame, textvariable=self.change_student).grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="ew")
        Button(query_frame, text='按序号查询', command=self.id_change).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        Button(query_frame, text='按姓名查询', command=self.name_change).grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        query_frame.grid_columnconfigure(1, weight=1)

        Label(self, textvariable=self.status_student).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # 信息显示和编辑区域
        info_frame = Frame(self)
        info_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        # 配置info_frame的行列
        for i in range(8):
            info_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            info_frame.grid_columnconfigure(j, weight=1)

        Label(info_frame, text='序   号 : ').grid(row=0, column=0, padx=5, pady=5, sticky="e")
        Entry(info_frame, textvariable=self.id, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        Label(info_frame, text='姓   名 : ').grid(row=1, column=0, padx=5, pady=5, sticky="e")
        Entry(info_frame, textvariable=self.name).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        Label(info_frame, text='分   类 : ').grid(row=2, column=0, padx=5, pady=5, sticky="e")
        # Entry(info_frame, textvariable=self.kulas).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    # 使用 Combobox 替换原来的 Entry
        self.kulas_combobox = ttk.Combobox(info_frame, textvariable=self.kulas, values=self.type_options, width=12, state="readonly")
        self.kulas_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        Label(info_frame, text='来   源 : ').grid(row=3, column=0, padx=5, pady=5, sticky="e")
        Entry(info_frame, textvariable=self.math).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        Label(info_frame, text='收 入 金 额 : ').grid(row=4, column=0, padx=5, pady=5, sticky="e")
        Entry(info_frame, textvariable=self.english).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        Label(info_frame, text='支 出 金 额 : ').grid(row=5, column=0, padx=5, pady=5, sticky="e")
        Entry(info_frame, textvariable=self.english_out).grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        Label(info_frame, text='日   期 : ').grid(row=6, column=0, padx=5, pady=5, sticky="e")
        # 使用 DateEntry 替代原来的 Entry
        self.computer_calendar = DateEntry(info_frame, textvariable=self.computer, date_pattern='yyyy.mm.dd', width=12)
        self.computer_calendar.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # 按钮区域
        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        Button(button_frame, text='修    改', command=self.update_student_info).pack(side=LEFT, padx=10)
        Button(button_frame, text='删    除', command=self.delete_student).pack(side=LEFT, padx=10)
        
        # 状态标签
        Label(self, textvariable=self.status_name, fg='red').grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # 新增 Listbox 控件用于显示查询到的多个同名学生信息
        listbox_frame = Frame(self)
        listbox_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        Label(listbox_frame, text="查询结果:").pack(anchor=W)
        self.listbox = Listbox(listbox_frame, width=30, height=10)
        self.listbox.pack(fill=BOTH, expand=True, pady=5)
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
        # 设置日期选择器的值
        date_str = student[6]
        if date_str:
            try:
                # 将字符串日期转换为日期对象并设置到 DateEntry
                date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                self.computer_calendar.set_date(date_obj)
            except ValueError:
                # 如果日期格式不正确，设置为当前日期
                self.computer_calendar.set_date(datetime.now())

    def update_student_info(self):
        student_id = self.id.get()
        if not student_id:
            self.status_name.set("未选择人员或id为空")
            return

        # 从 DateEntry 控件获取日期值
        try:
            date_value = self.computer_calendar.get()
            # 验证日期格式
            datetime.strptime(date_value, "%Y.%m.%d")
        except ValueError:
            self.status_name.set("日期格式错误")
            return

        # 获取分类值，如果使用了下拉框，这里会获取选中的值
        kulas_value = self.kulas.get().strip()
        
        # 可选：验证分类值是否在预定义选项中
        # if kulas_value and hasattr(self, 'type_options') and kulas_value not in self.type_options:
        #     # 如果需要严格验证，可以启用这段代码
        #     # self.status_name.set("分类值无效")
        #     # return
        #     pass  # 但通常我们允许用户输入或选择不在列表中的值

        new_data = (
            self.name.get(),
            kulas_value,  # 使用处理过的分类值
            self.math.get(),
            self.english.get(),
            self.english_out.get(),
            date_value  # 使用从 DateEntry 获取的日期值
        )

        flag, msg = mysql_student.update_student(student_id, new_data)
        if flag:
            self.status_name.set(msg)
            self.after(5000, lambda: self.status_name.set(""))  # 5 秒后清除
            # 更新 Listbox 内容
            self.update_listbox(mysql_student.search_name(self.change_student.get())[1])
        else:
            self.status_name.set(f"更新失败：{msg}")
            self.after(5000, lambda: self.status_name.set(""))  # 5 秒后清除

    def delete_student(self):
        student_id = self.id.get()
        if not student_id:
            self.status_name.set("未选择人员或id为空")
            return

        flag, msg = mysql_student.delete_id(student_id)
        if flag:
            self.status_name.set(msg)
            self.after(5000, lambda: self.status_name.set(""))  # 5 秒后清除
            # 更新 Listbox 内容
            self.update_listbox(mysql_student.search_name(self.change_student.get())[1])
            self.clear_details()
        else:
            self.status_name.set(f"删除失败：{msg}")
            self.after(5000, lambda: self.status_name.set(""))  # 5 秒后清除

    def clear_details(self):
        self.id.set("")
        self.name.set("")
        self.kulas.set("")
        self.math.set("")
        self.english.set("")
        self.english_out.set("")
        # 重置日期选择器为当前日期
        self.computer_calendar.set_date(datetime.now())
      
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
 