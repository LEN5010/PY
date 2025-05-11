import tkinter as tk
from tkinter import ttk
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
        self.geometry("600x450+230+200")
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
            self, text="返回",
            command=self.reset_interface,
            font=FONT,
            bg=COLORS["primary"],
            fg=COLORS["dark"],
            borderwidth=0
        )

        # 搞一个假的进度条
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")

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
            self.label.config(text="加密中...",)
            #开始加密
            self.label.pack(pady=(40,0))
            # 删掉之前的按钮
            self.start_button.pack_forget()
            self.input_text.pack_forget()
            self.input_key.pack_forget()
            self.id_label.pack_forget()
            self.wj_label.pack_forget()

            #在这里增加一个假的进度条
            self.progress.pack(pady=(20,20))
            for i in range(100):
                self.progress["value"] = i+1
                self.update()
                time.sleep(0.01)

            #加密完成
            self.label.config(text="加密完成")
            self.label.pack()

            # 点击按钮显示加密结果
            self.show_result_button.pack()

    def show_result(self):
        
        # 计算加密结果
        text = self.input_text.get()
        key = self.input_key.get()
        wj_result = vj_enc(text, key)
        ms_result = ms_enc(text)
        pg_result = pg_enc(text)
        
        # 移除之前的组件
        self.progress.pack_forget()
        self.show_result_button.pack_forget()

        # 显示解密标题
        self.label.config(text="加密结果:",font=HEADER_FONT, bg=COLORS["bg"])
        self.label.pack(pady=30)

        # 显示解密结果
        self.result_wj = tk.Label(self, text="维吉尼亚密码: "+wj_result, font=FONT, bg=COLORS["bg"])
        self.result_wj.pack(pady=10)
        self.result_ms = tk.Label(self, text="莫斯密码: "+ms_result, font=FONT, bg=COLORS["bg"])
        self.result_ms.pack(pady=10)
        self.result_pg = tk.Label(self, text="培根密码: "+pg_result, font=FONT, bg=COLORS["bg"])
        self.result_pg.pack(pady=10)


        self.back_button.pack(pady=10)
    
    def reset_interface(self):
        #重置界面，恢复输入状态
        self.back_button.pack_forget()
        self.result_wj.pack_forget()
        self.result_ms.pack_forget()
        self.result_pg.pack_forget()
        self.label.pack_forget()
        self.id_label.pack(pady=(30, 0))
        self.input_text.pack(pady=20)
        self.wj_label.pack()
        self.input_key.pack(pady=20)
        self.start_button.pack(pady=10)

# 计算维吉尼亚加密
def vj_enc(text, key):
    enc_result = []
    key_index = 0
    key = key.upper()
    
    for char in text:
        if char.isalpha():
            # 计算位移量（密钥字母对应的数值）
            shift = ord(key[key_index % len(key)]) - ord('A')
            # 加密处理（区分大小写）
            if char.isupper():
                enc_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                enc_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            key_index += 1
        else:
            enc_char = char  # 非字母字符保持不变
        enc_result.append(enc_char)
    
    return ''.join(enc_result)

# 计算摩斯密码加密
def ms_enc(text):
    ms_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
        ' ': '/'  # 单词分隔符
    }
    
    enc_result = []
    for char in text.upper():
        if char in ms_code:
            enc_result.append(ms_code[char])
        else:
            enc_result.append(char)  # 非字母数字保持不变
    
    return ' '.join(enc_result)  # 字符间用空格分隔

# 计算培根密码加密
def pg_enc(text):
    pg_code = {
        'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
        'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
        'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
        'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
        'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab'
    }
    
    pg_result = []
    for char in text.upper():
        if char.isalpha():
            pg_result.append(pg_code.get(char, char))
        else:
            pg_result.append(char)  # 非字母字符保持不变
    return ''.join(pg_result)

if __name__ == "__main__":
    app = App()
    app.mainloop()