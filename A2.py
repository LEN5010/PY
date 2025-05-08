import tkinter as tk
import random,hashlib,json
from tkinter import messagebox
import datetime

COLORS = {
    "bg": "#F0F4F8",           # 背景色
    "primary": "#1A73E8",      # 主色调
    "secondary": "#34A853",    # 次要色调
    "accent": "#EA4335",       # 强调色
    "light": "#FFFFFF",        # 浅色
    "dark": "#202124",         # 深色
    "border": "#DADCE0"        # 边框色
}

FONT = ("/Users/len5010/Desktop/code/PY/data/SourceHanSansHWSC-Regular.otf", 12)
HEADER_FONT = ("/Users/len5010/Desktop/code/PY/data/SourceHanSansHWSC-Regular.otf", 14, "bold")

class App(tk.Tk):

    def __init__(self,que,rnk):
        super().__init__()
        self.title("猜谜")
        self.geometry("630x400+230+200")
        self.configure(bg=COLORS["bg"]) 
        # 创建窗口

        self.score = 10
        self.que_now = None
        self.time = None
        self.difficulty = tk.StringVar()     # 追踪dif的值
        self.difficulty.set("简单")          # 避免没有初始的选择
        self.questions = que
        self.ranking = rnk 
        self.is_time_running = False       # 这个用来判断时间减少逻辑是否运行过了
        self.player_id = None             # 用户id
        # 初始化

        difficulty_label = tk.Label(self, text="选择难度:", font=FONT, bg=COLORS["bg"])
        # 难度选择标签
        self.difficulty_label = difficulty_label
        # 这个用来调用forget
        difficulty_label.pack()

        difficulty_menu = tk.OptionMenu(self, self.difficulty, "简单", "中等", "困难")
        difficulty_menu.config(font=FONT, bg=COLORS["light"], fg=COLORS["dark"])
        # 难度选择按钮
        self.difficulty_menu = difficulty_menu
        # 这个用来调用forget
        difficulty_menu.pack(pady =5)

        id_label = tk.Label(self, text="输入你的ID:", font=FONT, bg=COLORS["bg"])
        # 输入ID标签
        self.id_label = id_label
        # 这个用来调用forget
        id_label.pack()

        your_id = tk.Entry(self, font=FONT, bg=COLORS["light"], fg=COLORS["dark"])
        # 输入玩家id
        self.your_id = your_id
        # 这个用来调用forget
        your_id.pack()

        start_button = tk.Button(
            self,
            text="开始游戏",
            command=self.start_game,
            font=FONT,
            bg=COLORS["primary"],
            fg=COLORS["dark"],
            activebackground=COLORS["secondary"],
            highlightbackground=COLORS["primary"],
            borderwidth=0
            )
        self.start_button = start_button
        # 开始按钮标签
        # 这个用来调用forget
        start_button.pack(pady= 10)

        self.show_ranking()
        #显示排行榜

        self.label = tk.Label(self, text="", font=HEADER_FONT, bg=COLORS["bg"])
        # 显示谜题
        self.ipt_ans = tk.Entry(self, font=FONT, bg=COLORS["light"], fg=COLORS["dark"])
        # 输入框
        self.button = tk.Button(self, text="提交答案", 
                                command=self.on_click,
                                font=FONT, bg=COLORS["primary"],
                                fg=COLORS["light"],
                                activebackground=COLORS["secondary"])
        # 提交答案
        self.score_label = tk.Label(self, text=f"当前分数: {self.score}",bg=COLORS["bg"])
        # 积分
        self.quit_button = tk.Button(self, text="退出游戏", 
                                     command=self.quit_game,
                                     font=FONT,
                                     bg=COLORS["accent"],
                                     fg=COLORS["light"],
                                     activebackground=COLORS["secondary"])
        # 退出按钮
        self.time_label = tk.Label(self, text=f"当前剩余时间: {self.time}", 
                                   font=FONT,
                                   bg=COLORS["bg"])
        # 剩余时间

    def start_game(self): 
        player_id = self.your_id.get().strip()
        if not player_id:
            messagebox.showinfo("提示", "请输入你的ID")
            return
        else:
            self.player_id = player_id      #测试了很多次,这里要先保存一下id,因为之前的id输入框会被删除,没法调用了
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
            self.ranking_frame.pack_forget()
            self.start_button.pack_forget()
            self.difficulty_menu.pack_forget()
            self.your_id.pack_forget()
            self.id_label.pack_forget()
            self.difficulty_label.pack_forget()
            # 开始计算时间
            self.time = self.time_limit()
            if self.is_time_running == False:
                self.is_time_running = True
                self.time_continue()
            # 只调用一次时间计算逻辑,否则答n题之后会每秒减少n个时间

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
            self.start_game()
        elif self.difficulty.get() == "中等":
            messagebox.showinfo("提示", "回答错误！")
            self.score -= 2
            self.score_label.config(text=f"当前分数: {self.score}")
            self.start_game()
        elif self.difficulty.get() == "困难":
            messagebox.showinfo("提示", "回答错误！")
            self.score -= 3
            self.score_label.config(text=f"当前分数: {self.score}")
            self.start_game()
        # 分数是否为负数
        if self.score <= 0:
            messagebox.showinfo("提示", "游戏结束！")
            self.quit_game()

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
            self.quit_game()

    def save_score(self):
        # 检查当前分数是否可以进入排行榜
        min_rank_index = -1
        
        for i, rank_data in enumerate(self.ranking):
        # 空位置直接插入
            if rank_data["score"] is None:
                min_rank_index = i  # 优先填充靠前的空位置
                break  # 找到第一个空位置，空位置应按排名顺序填充
            # 处理有分数的位置：若当前分数更高，则记录位置
            elif self.score > rank_data["score"]:
                if min_rank_index == -1:
                    min_rank_index = i  # 记录分数更高的位置
                    break
        
        # 如果可以进入排行榜
        if min_rank_index != -1:
            # 将排行榜中的记录后移
            for i in range(len(self.ranking) - 1, min_rank_index, -1):
                self.ranking[i] = self.ranking[i-1].copy()
                self.ranking[i]["rank"] = str(int(self.ranking[i]["rank"]) + 1)
            # 插入新记录
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.ranking[min_rank_index] = {
                "rank": str(min_rank_index + 1),
                "date": current_date,
                "player_id": self.player_id,  # 使用保存的ID
                "score": self.score
            }
            # 保存到文件
            try:
                with open("/Users/len5010/Desktop/code/PY/data/A2_puzze/ranking.json", "w", encoding="utf-8") as f:
                    json.dump(self.ranking, f, ensure_ascii=False, indent=4)
                return True
            except Exception as e:
                print(f"保存排行榜失败: {e}")
                return False
        return False

    def show_ranking(self):
        # 创建排行榜框架
        ranking_frame = tk.Frame(self,bg=COLORS["bg"])
        ranking_frame.pack(pady=10)
        self.ranking_frame = ranking_frame
        
        # 排行榜标题
        rank_title = tk.Label(
        ranking_frame, 
        text="排行榜", 
        font=("Arial", 14, "bold"),
        bg=COLORS["bg"]  # 添加背景色
        )
        rank_title.grid(row=0, column=0, columnspan=3, pady=5)
        
        # 排行榜表头
        headers = ["排名", "玩家ID", "分数","日期"]
        for i, header in enumerate(headers):
            for i, header in enumerate(headers):tk.Label(
                ranking_frame, 
                text=header, 
                font=("Arial", 10, "bold"),
                bg=COLORS["bg"]  # 添加背景色
            ).grid(row=1, column=i, padx=15)
        
        # 显示排行榜数据
        for i, rank_data in enumerate(self.ranking):
            row_bg = COLORS["bg"]  # 统一一下背景色
            
            if rank_data["score"] is not None:
                tk.Label(ranking_frame, text=rank_data["rank"], bg=row_bg).grid(row=i+2, column=0)
                tk.Label(ranking_frame, text=rank_data["player_id"], bg=row_bg).grid(row=i+2, column=1)
                tk.Label(ranking_frame, text=str(rank_data["score"]), bg=row_bg).grid(row=i+2, column=2)
                tk.Label(ranking_frame, text=str(rank_data["date"]), bg=row_bg).grid(row=i+2, column=3)
            else:
                tk.Label(ranking_frame, text=rank_data["rank"], bg=row_bg).grid(row=i+2, column=0)
                tk.Label(ranking_frame, text="---", bg=row_bg).grid(row=i+2, column=1)
                tk.Label(ranking_frame, text="---", bg=row_bg).grid(row=i+2, column=2)
                tk.Label(ranking_frame, text="---", bg=row_bg).grid(row=i+2, column=3)

    def quit_game(self):
        # 保存分数
        if self.score > 0:
            result = self.save_score()
            if result:
                messagebox.showinfo("提示", f"恭喜！你的分数 {self.score} 已进入排行榜！")
        # 销毁窗口
        self.destroy()
        
def load_questions():
    try:
        with open("/Users/len5010/Desktop/code/PY/data/A2_puzze/puzzle.json", "r", encoding="utf-8") as f:
            questions = json.load(f)  # 读取为Python列表（包含字典）
        return questions
    except FileNotFoundError:
        return []  # 文件不存在返回空列表  

def load_rank():
    try:
        with open("/Users/len5010/Desktop/code/PY/data/A2_puzze/ranking.json", "r", encoding="utf-8") as f:
            ranking = json.load(f)  # 读取为Python列表（包含字典）
        return ranking
    except FileNotFoundError:
        return []  # 文件不存在返回空列表  

if __name__ == "__main__":
    que = load_questions()
    rnk = load_rank()
    app = App(que,rnk)
    app.mainloop()