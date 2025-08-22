# MianPgae.py - 修正后的版本
from tkinter import *
from views import ChangeFrame, InsertFrame, SearchFrame, HelpFrame
import mysql_student
import keyboard


class MianPage:
    def __init__(self, master):
        self.root = master
        self.root.title('郓城东盛纺织账目管理系统')
        self.root.geometry('800x290')

        # 创建一个主容器Frame，统一使用grid布局
        self.main_container = Frame(self.root)
        self.main_container.pack(fill=BOTH, expand=True)

        # 配置主容器的网格权重
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.create_page()

    def create_page(self):
        # 创建各个功能页面
        self.insert_frame = InsertFrame(self.main_container)
        self.search_frame = SearchFrame(self.main_container)
        self.change_frame = ChangeFrame(self.main_container)  # 确保ChangeFrame支持grid
        self.help_frame = HelpFrame(self.main_container)

        # 使用 grid 布局管理 Frame，并设置 sticky="nsew"
        self.insert_frame.grid(row=0, column=0, sticky="nsew")
        self.search_frame.grid(row=0, column=0, sticky="nsew")
        self.change_frame.grid(row=0, column=0, sticky="nsew")
        self.help_frame.grid(row=0, column=0, sticky="nsew")

        # 默认隐藏其他 Frame
        self.search_frame.grid_remove()
        self.change_frame.grid_remove()
        self.help_frame.grid_remove()

        # 创建菜单栏
        menubar = Menu(self.root, tearoff=False)
        menubar.add_command(label=' 录 入 ', command=self.show_insert)

        submenu_search = Menu(menubar, tearoff=False)
        submenu_search.add_command(label='降   序', command=self.show_search_sort_down, accelerator="Ctrl + J")
        submenu_search.add_separator()
        submenu_search.add_command(label='序   号', command=self.show_search_id, accelerator="Ctrl + D")
        submenu_search.add_command(label='类   型', command=self.show_search_total, accelerator="Ctrl + T")
        submenu_search.add_command(label='金   额', command=self.show_search_math, accelerator="Ctrl + M")
        submenu_search.add_command(label='日   期', command=self.show_search_computer, accelerator="Ctrl + S")

        menubar.add_cascade(label=' 查 询 ', menu=submenu_search)
        menubar.add_command(label=' 修 改 ', command=self.show_change)
        menubar.add_command(label=' 帮 助 ', command=self.show_help)

        self.root.config(menu=menubar)

        # 右键菜单功能
        def xShowMenu(event):
            menubar.post(event.x_root, event.y_root)

        self.root.bind("<Button-3>", xShowMenu)
        self.show_insert()

    def show_insert(self):
        self.insert_frame.grid()
        self.search_frame.grid_remove()
        self.change_frame.grid_remove()
        self.help_frame.grid_remove()

    def show_search(self):
        self.insert_frame.grid_remove()
        self.change_frame.grid_remove()
        self.help_frame.grid_remove()
        self.search_frame.grid()
        self.search_frame.show_search_data()

    def show_change(self):
        self.insert_frame.grid_remove()
        self.search_frame.grid_remove()
        self.help_frame.grid_remove()
        self.change_frame.grid()

    def show_help(self):
        self.insert_frame.grid_remove()
        self.search_frame.grid_remove()
        self.change_frame.grid_remove()
        self.help_frame.grid()

    def show_search_sort_down(self):
        mysql_student.sort_student ^= 1
        self.show_search()

    def show_search_id(self):
        mysql_student.sort_data = 0
        self.show_search()

    def show_search_total(self):
        mysql_student.sort_data = 1
        self.show_search()

    def show_search_math(self):
        mysql_student.sort_data = 2
        self.show_search()

    def show_search_computer(self):
        mysql_student.sort_data = 4
        self.show_search()