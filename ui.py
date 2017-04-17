import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox, Listbox
import requests
from spider import get_serach_item
from config import headers


class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # 有点相当于tk.Tk()
        self.topframe = tk.Frame(self, height=80)
        self.contentframe = tk.Frame(self, height=720)
        self.dirname = os.getcwd()
        self.gentry1 = tk.Label(self.topframe, text=self.dirname)
        self.entryvar = tk.StringVar()
        self.rightbar = tk.Scrollbar(self.contentframe, orient=tk.VERTICAL)
        self.bottombar = tk.Scrollbar(self.contentframe, orient=tk.HORIZONTAL)
        self.listbox = tk.Listbox(self.contentframe, yscrollcommand=self.rightbar.set,
                                  xscrollcommand=self.bottombar.set,
                                  height=720,
                                  width=800)
        self.createWidgets()

    def createWidgets(self):
        self.title('电影种子下载小程序')
        # 设置800*400大小且居中
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (800, 400, (screenwidth - 800) / 2, (screenheight - 400) / 2)
        self.geometry(size)
        self.topframe.pack(side=tk.TOP)
        glabel1 = tk.Label(self.topframe, text='请选择下载路径:')
        gbutton1 = tk.Button(self.topframe, text='选择', command=self.__choose_dir)
        glabel1.grid(row=0, column=0, sticky=tk.W)
        self.gentry1.grid(row=0, column=1)
        gbutton1.grid(row=0, column=2)
        glabel2 = tk.Label(self.topframe, text='请输入搜索的电影名:')
        gentry2 = tk.Entry(self.topframe, textvariable=self.entryvar)
        gbutton2 = tk.Button(self.topframe, text='搜索', command=self.__search_movie)
        glabel2.grid(row=1, column=0, sticky=tk.W)
        gentry2.grid(row=1, column=1)
        gbutton2.grid(row=1, column=2)
        self.contentframe.pack()
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.rightbar.config(command=self.listbox.yview)
        self.bottombar.config(command=self.listbox.xview)

    def addmenu(self, Menu):
        Menu(self)

    def __choose_dir(self):
        self.dirname = filedialog.askdirectory()
        self.gentry1['text'] = self.dirname
        if not self.dirname:
            messagebox.showwarning('警告', message='未选择文件夹！')

    def __search_movie(self):
        if self.entryvar.get():
            self.listbox.delete(0, tk.END)  # 先删除所有
            messagebox.showinfo('提醒', '因为资源是在线爬取，搜索会有卡顿，见谅！')
            self.abc = get_serach_item(self.entryvar.get())
            if self.abc:
                for item in self.abc:
                    self.listbox.insert(len(self.abc), item['title'])
                self.listbox.bind('<Button-2>', self.popmenu)
                self.menu = tk.Menu(self, tearoff=0)
                self.menu.add_command(label="下载", command=self.downitem)
                self.menu.add_separator()
                self.menu.add_command(label="取消")
            else:
                messagebox.showinfo('提醒', '抱歉暂时没搜索到相关资源')
        else:
            messagebox.showinfo('提醒', '搜索内容不能为空')

    def popmenu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def downitem(self):
        url = self.abc[self.listbox.curselection()[0]]['url']  # url链接
        name = self.abc[self.listbox.curselection()[0]]['title']
        messagebox.showinfo('提醒', name + '开始下载')
        r = requests.get(url, headers=headers)
        with open(self.dirname + '/' + name + 'torrent', 'wb') as f:
            f.write(r.content)


class MyMenu():
    def __init__(self, root):
        self.menubar = tk.Menu(root)  # 创建菜单栏
        mymenu = tk.Menu(self.menubar, tearoff=0)
        mymenu.add_command(label="关于", command=self.my_about)
        mymenu.add_separator()
        mymenu.add_command(label="退出", command=root.quit)
        # 将菜单添加到菜单栏
        self.menubar.add_cascade(label="菜单", menu=mymenu)
        # 最后再将菜单栏整个加到窗口 root
        root.config(menu=self.menubar)

    def my_about(self):
        messagebox.showinfo('关于', '关于相关！')  # 消息提示框
        pass


if __name__ == '__main__':
    app = Application()
    app.addmenu(MyMenu)
    app.mainloop()
