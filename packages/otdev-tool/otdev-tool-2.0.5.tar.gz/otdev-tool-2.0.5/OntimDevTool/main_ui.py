import json
import hashlib
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from OntimDevTool import G_version, get_password, set_password
from OntimDevTool.diag_port_controller import open_diag_port, close_diag_port
from OntimDevTool.auth_controller import authorise, edl, offline_auth_01_get_nonce, offline_auth_02_get_sign, offline_auth_03_set_permission

FUNCTIONLIST = ["open_diag", "close_diag", "authorise", "edl"]
MODELLIST = ["cursader_tf", "sunfire", "venom", "shadow_tmo", "shadow_row"]

class App():
    def __init__(self, master):
        self.master = master
        self.master.title(f"otdev-tool {G_version}")
        self.master.resizable(width=False, height=False)  # 窗口大小不可变
        print(f"cyqq {get_password}")

        # 把主窗口显示到屏幕中央
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 360
        window_height = 360
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建修改密码菜单
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        password_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="文件", menu=password_menu)
        password_menu.add_command(label="修改密码", command=self.on_change_password)

        group1 = tk.LabelFrame(self.master, text="Online")
        group1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.55)

        # 左边的列表框和标签
        self.lbl_model_selection = tk.Label(self.master)
        self.lbl_model_selection.grid(row=0, column=1, padx=0, pady=0, sticky="W")
        self.lbl_model = tk.Label(self.master, text="请选择手机型号")
        self.lbl_model.grid(row=1, column=0, padx=10, pady=5, sticky="W")
        self.lb_model = tk.Listbox(self.master, height=4, selectmode="single")
        self.lb_model.grid(row=2, column=0, padx=10, pady=5)
        self.lb_model.config(exportselection=False)


        # 给列表框添加垂直滚动条
        scrollbar = tk.Scrollbar(self.master, command=self.lb_model.yview)
        scrollbar.grid(row=2, column=0, sticky="nse", pady=5)
        self.lb_model.config(yscrollcommand=scrollbar.set)

        # 从变量中获取列表项目
        for item in MODELLIST:
            self.lb_model.insert("end", item)
        self.lb_model.bind("<<ListboxSelect>>", self.on_select_model)

        # 右边的列表框和标签
        self.lbl_func_selection = tk.Label(self.master)
        self.lbl_func_selection.grid(row=0, column=1, padx=0, pady=0, sticky="W")
        self.lbl_func = tk.Label(self.master, text="请选择功能")
        self.lbl_func.grid(row=1, column=1, padx=15, pady=0, sticky="W")  # 左端对齐
        self.lb_func = tk.Listbox(self.master, height=4, selectmode="single")
        self.lb_func.grid(row=2, column=1, padx=15, pady=0)

        # 给列表框添加垂直滚动条
        scrollbar = tk.Scrollbar(self.master, command=self.lb_func.yview)
        scrollbar.grid(row=2, column=1, sticky="nse", pady=5)
        self.lb_func.config(yscrollcommand=scrollbar.set)

        # 从变量中获取列表项目
        for item in FUNCTIONLIST:
            self.lb_func.insert("end", item)
        self.lb_func.bind("<<ListboxSelect>>", self.on_select_func)

        # 确认和退出按钮
        self.btn_ok = tk.Button(self.master, text="确认", command=self.on_ok)
        self.btn_ok.grid(row=4, column=0, padx=10, pady=10)
        self.btn_cancel = tk.Button(self.master, text="退出", command=self.master.quit)
        self.btn_cancel.grid(row=4, column=1, padx=10, pady=10)

        self.selected_func = None
        self.selected_model = None

        # Create a frame for the third group
        group2 = tk.LabelFrame(self.master, text="Offline")
        group2.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.4)

        # Add a big text area to the third group
        self.text_area = tk.Text(group2, height=5)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create three buttons for the third group
        self.button1 = tk.Button(group2, text="1. Get Nonce", command=self.on_get_nonce)
        self.button1.pack(side=tk.LEFT, padx=5, pady=5)

        self.button2 = tk.Button(group2, text="2. Get Sign", command=self.on_get_sign)
        self.button2.pack(side=tk.LEFT, padx=5, pady=5)

        self.button3 = tk.Button(group2, text="3. Set Permission", command=self.on_set_permission)
        self.button3.pack(side=tk.LEFT, padx=5, pady=5)

    def on_select_func(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_func = event.widget.get(index)
            self.lbl_func.config(text=f"功能：{self.selected_func}")

    def on_select_model(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_model = event.widget.get(index)
            self.lbl_model.config(text=f"手机型号：{self.selected_model}")

    def on_ok(self):
        if not self.selected_func or not self.selected_model:
            messagebox.showerror("错误", "请选择功能和手机型号")
            return
        
        try:
            if self.selected_func == FUNCTIONLIST[0]:
                open_diag_port(self.selected_model)
            elif self.selected_func == FUNCTIONLIST[1]:
                close_diag_port()
            elif self.selected_func == FUNCTIONLIST[2]:
                authorise(self.selected_model)
            elif self.selected_func == FUNCTIONLIST[3]:
                edl(self.selected_model)
        except subprocess.TimeoutExpired:
            messagebox.showinfo("执行失败", f"{self.selected_func} 功能执行失败，请确认手机在fastboot模式，且已连接usb线。\n")
            return
        except Exception as e:
            messagebox.showinfo("执行失败", f"{self.selected_func} 功能执行失败\n, 错误信息：{repr(e)}")
            return
        messagebox.showinfo("执行成功", f"{self.selected_func} 功能执行成功！")
    
    def on_get_nonce(self):
        nonce = offline_auth_01_get_nonce()
        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", nonce)
    
    def on_get_sign(self):
        sign = offline_auth_02_get_sign(self.text_area.get("1.0", "end"), self.selected_model)
        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", sign)


    def on_set_permission(self):
        offline_auth_03_set_permission(self.text_area.get("1.0", "end"))
        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", "Authentication success.")
    
    def on_change_password(self):
        # 弹出修改密码对话框
        new_password = askstring("修改管理员密码", "请输入新密码：", show="*")
        if new_password:
            # 保存密码，并显示密码已修改
            set_password(new_password)
            with open('authorization.json', 'r') as f:
                authorization = json.load(f)
                md5 = hashlib.md5(new_password.encode("ascii"))
                password_md5 = md5.hexdigest()
                authorization["password"] = password_md5
            with open("users.json", "w") as f:
                json.dump(authorization, f)
            tk.messagebox.showinfo(title="密码已修改", message="管理员密码已修改！")


def main():
    from OntimDevTool.login_ui import LoginWindow
    root = tk.Tk()
    login_window = LoginWindow(root)
    login_window.mainloop()


if __name__ == "__main__":
    main()
