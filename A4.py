import tkinter as tk
import random,hashlib,json
from tkinter import messagebox
import datetime,os,time

COLORS = {
    "bg": "#F0F4F8",           # 背景色
    "primary": "#1A73E8",      # 主色调
    "secondary": "#34A853",    # 次要色调
    "accent": "#EA4335",       # 强调色
    "light": "#FFFFFF",        # 浅色
    "dark": "#202124",         # 深色
    "border": "#DADCE0"        # 边框色
}

# 使用相对路径设置,这里改成os.path.join,这样其他系统也可以运行
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录
FONT_PATH = os.path.join(BASE_DIR, 'data', 'SourceHanSansHWSC-Regular.otf')
FONT = (FONT_PATH, 12)
SMALL_FONT = (FONT_PATH, 10)
HEADER_FONT = (FONT_PATH, 14, "bold")

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("神秘密码程序")
        self.geometry("500x350+230+200")
        self.configure(bg=COLORS["bg"]) 
        # 创建窗口

        # 初始化

        id_label = tk.Label(self, text="输入一段英文字符:", font=FONT, bg=COLORS["bg"])
        # 输入字符
        self.id_label = id_label
        # 这个用来调用forget
        id_label.pack(pady=(30,0))

        input_text = tk.Entry(self, font=FONT, bg=COLORS["light"], fg=COLORS["dark"],width=40)
        # 输入玩家id
        self.input_text = input_text
        # 这个用来调用forget
        input_text.pack(pady=20)

        wj_label = tk.Label(self, text="输入密钥:", font=SMALL_FONT, bg=COLORS["bg"])
        # 输入维吉尼亚密钥标签
        self.wj_label = wj_label
        # 这个用来调用forget
        wj_label.pack()

        input_key = tk.Entry(self, font=FONT, bg=COLORS["light"], fg=COLORS["dark"],width=4)
        # 输入维吉尼亚密钥
        self.input_key = input_key
        # 这个用来调用forget
        input_key.pack(pady=20)

        back_button = tk.Button(
            self, text="返回", command=self.reset_interface,
            bg=COLORS["primary"], fg=COLORS["dark"], borderwidth=0
        )
        # 写一个返回逻辑
        self.back_button = back_button
        # 这个用来调用forget

        start_button = tk.Button(
            self,
            text="开始进行加密",
            command=self.start_jm,
            font=FONT,
            bg=COLORS["primary"],
            fg=COLORS["dark"],
            borderwidth=0
            )
        self.start_button = start_button
        # 这个用来调用forget
        start_button.pack(pady= 10)
        self.label = tk.Label(self, text="", font=HEADER_FONT, bg=COLORS["bg"])

        show_result_button = tk.Button(
            self,
            text="显示解密结果",
            command=self.show_result,
            bg=COLORS["primary"],
            fg=COLORS["dark"],
            borderwidth=0
            )
        self.show_result_button = show_result_button

    def start_jm(self):
        text = self.input_text.get()
        key = self.input_key.get()
        if (not text) or (not key):
            messagebox.showinfo("提示", "请输入字符或密钥!")
            return
        else:
            self.label.config(text="解密中",)
            #开始解密
            self.label.pack(pady=(40,0))
            # 删掉之前的按钮
            self.start_button.pack_forget()
            self.input_text.pack_forget()
            self.input_key.pack_forget()
            self.id_label.pack_forget()
            self.wj_label.pack_forget()

            #调用计算逻辑(之后实现)
            #compute_enc(text,key)

            #在这里增加一个假的进度条
            for i in range(100):
                self.label.config(text=f"解密中{i}%")
                self.update()
                time.sleep(0.01)

            #解密完成
            self.label.config(text="解密完成")
            self.label.pack()

            # 点击按钮显示解密结果
            self.show_result_button.pack()

    def show_result(self):

        # 移除之前的组件
        self.show_result_button.pack_forget()

        # 显示解密结果
        self.label.config(text="解密结果")
        self.label.pack(pady=30)

        self.back_button.pack(pady=10)
    
    def reset_interface(self):
        #重置界面，恢复输入状态
        self.back_button.pack_forget()
        self.label.pack_forget()
        self.id_label.pack(pady=(30, 0))
        self.input_text.pack(pady=20)
        self.wj_label.pack()
        self.input_key.pack(pady=20)
        self.start_button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()