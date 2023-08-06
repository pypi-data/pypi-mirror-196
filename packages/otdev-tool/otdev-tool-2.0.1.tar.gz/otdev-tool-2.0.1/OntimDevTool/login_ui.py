import tkinter as tk
from tkinter import messagebox
import hashlib
from OntimDevTool.main_ui import App
from OntimDevTool import get_password, set_password

class LoginWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("用户登录")
        # self.master.resizable(width=False, height=False)  # 窗口大小不可变

        # 把主窗口显示到屏幕中央
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 230
        window_height = 110
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建用户名标签和输入框
        self.username_label = tk.Label(self.master, text="用户名：")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=0, pady=10, sticky="W")
        self.username_entry.insert(0, "admin")

        # 创建密码标签和输入框
        self.password_label = tk.Label(self.master, text="密码：")
        self.password_label.grid(row=1, column=0, padx=10, pady=0, sticky="W")
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=0, pady=0)
        # 绑定回车键事件，当用户在密码框中按下回车键时，执行login函数
        self.password_entry.bind("<Return>", self.login)

        # 创建登录按钮
        self.login_button = tk.Button(self.master, text="登录", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # self.master.columnconfigure(1, weight=1)
        # self.master.rowconfigure(0, weight=1)

    def login(self):
        # 获取用户名和密码
        password = self.password_entry.get()
        md5 = hashlib.md5(password.encode("ascii"))
        password_md5 = md5.hexdigest()

        # 验证用户名和密码
        if password_md5 == get_password():
            # 登录成功，打开新窗口（主界面）
            set_password(password)  #密码更新为明文，之后登录auth服务器时要使用
            self.master.destroy()
            root = tk.Tk()
            app = App(root)
        else:
            # 密码错误，弹出对话框提示用户重新输入
            messagebox.showerror("登录失败", "用户名或密码错误，请重新输入！")


if __name__ == "__main__":
    # 创建登录窗口
    root = tk.Tk()
    login_window = LoginWindow(root)
    login_window.mainloop()
