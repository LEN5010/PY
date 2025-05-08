import tkinter as tk
import random
from tkinter import messagebox
import hashlib
import json

class App(tk.Tk):

    def __init__(self,que):
        super().__init__()
        self.title("猜谜")
        self.geometry("600x400+430+300")
        # 创建窗口

        self.score = 10
        self.que_now = None
        self.time = None
        self.difficulty = tk.StringVar()       #追踪dif的值
        self.difficulty.set("简单")           #避免没有初始的选择
        self.questions = que
        # 初始化

        start_button = tk.Button(self, text="开始游戏", command=self.start_game)
        self.start_button = start_button
        # 开始按钮标签
        # 这个用来调用forget
        start_button.pack()

        difficulty_label = tk.Label(self, text="选择难度:")
        # 难度选择标签
        self.difficulty_label = difficulty_label
        # 这个用来调用forget
        difficulty_label.pack()

        difficulty_menu = tk.OptionMenu(self, self.difficulty, "简单", "中等", "困难")
        # 难度选择按钮
        self.difficulty_menu = difficulty_menu
        # 这个用来调用forget
        difficulty_menu.pack()


        self.label = tk.Label(self,text="")
        # 显示谜题
        self.ipt_ans = tk.Entry(self)
        # 输入框
        self.button = tk.Button(self,text="提交答案",command=self.on_click)
        # 提交答案
        self.score_label = tk.Label(self, text=f"当前分数: {self.score}")
        # 积分
        self.quit_button = tk.Button(self, text="退出游戏", command=self.quit)
        # 退出按钮
        self.time_label = tk.Label(self, text=f"当前剩余时间: {self.time}")
        # 剩余时间

    def start_game(self):
        
        # 初始化
        self.puzzle = self.get_random_que()
        self.label.config(text=self.puzzle["puz_name"])
        # 显示谜题
        self.label.pack()
        self.ipt_ans.pack()
        self.button.pack()
        self.score_label.pack()
        self.quit_button.pack()
        self.time_label.pack()
        # 删掉之前的按钮
        self.start_button.pack_forget()
        self.difficulty_menu.pack_forget()
        # 开始计算时间
        self.time = self.time_limit()
        self.time_continue()


    def get_random_que(self):
        fque = [q for q in self.questions if q["puz_dif"] == self.difficulty.get()]
        return random.choice(fque)

    def on_click(self):
        input_text = self.ipt_ans.get()
        ans_hash = hashlib.sha256(input_text.encode()).hexdigest()
        if ans_hash == self.puzzle["puz_hash"]:
            if self.difficulty.get() == "简单":
                self.score += 1
            elif self.difficulty.get() == "中等":
                self.score += 2
            elif self.difficulty.get() == "困难":
                self.score += 3
            self.score_label.config(text=f"当前分数: {self.score}")
            messagebox.showinfo("提示", "回答正确！")
            # 重新开始游戏
            self.start_game()
            #这部分是扣分逻辑,分别扣 1 2 3 分
        elif self.difficulty.get() == "简单":
            messagebox.showinfo("提示", "回答错误！")
            self.score -= 1
            self.score_label.config(text=f"当前分数: {self.score}")
        elif self.difficulty.get() == "中等":
            messagebox.showinfo("提示", "回答错误！")
            self.score -= 2
            self.score_label.config(text=f"当前分数: {self.score}")
        elif self.difficulty.get() == "困难":
            messagebox.showinfo("提示", "回答错误！")
            self.score -= 3
            self.score_label.config(text=f"当前分数: {self.score}")
        # 分数是否为负数
        if self.score <= 0:
            messagebox.showinfo("提示", "游戏结束！")
            self.quit()

        # 根据难度设置时间
    def time_limit(self):
        if self.difficulty.get() == "简单":
            return 30
        elif self.difficulty.get() == "中等":
            return 20
        else:
            return 10
        
        # 这个方法是用来倒计时的
    def time_continue(self):
        if self.time > 0:
            self.time -= 1
            self.after(1000, self.time_continue)
            self.time_label.config(text=f"当前剩余时间: {self.time}")
        else:
            messagebox.showinfo("提示", "时间到！")
            self.quit()
        
def load_questions():
    try:
        with open("/Users/len5010/Desktop/code/PY/data/A2_puzze/puzzle.json", "r", encoding="utf-8") as f:
            questions = json.load(f)  # 读取为Python列表（包含字典）
        return questions
    except FileNotFoundError:
        return []  # 文件不存在返回空列表  

if __name__ == "__main__":

    que = load_questions()
    app = App(que)
    app.mainloop()