import jieba,os,matplotlib,re,collections
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
from PIL import Image, ImageDraw
from matplotlib.font_manager import FontProperties

# 设置文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录
DATA_DIR = os.path.join(BASE_DIR, 'data/A3')  # 数据目录，存放文本文件
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')  # 输出目录，存放生成的图片
os.makedirs(OUTPUT_DIR, exist_ok=True)  # 确保输出目录存在，不存在则创建

# 设置字体和自定义词典
FONT_PATH = os.path.join(BASE_DIR, 'data/SourceHanSansHWSC-Regular.otf')
DICT_PATH = os.path.join(DATA_DIR, '自定义词典.txt')

# 读取西游记文本
with open(os.path.join(DATA_DIR, '西游记.txt'), 'r', encoding='gb18030') as f:
    content = f.read()  # 读取全部内容到content变量

# 建立人物别名字典，用于将不同称呼映射到标准人物名称
name_dict = {
    '唐僧': ['唐僧', '唐三藏', '玄奘', '金蝉子', '三藏'],
    '孙悟空': ['孙悟空', '悟空', '齐天大圣', '美猴王', '猴王', '孙行者', '行者', '猴子'],
    '猪八戒': ['猪八戒', '八戒', '悟能', '猪刚鬣', '天蓬元帅'],
    '沙僧': ['沙僧', '沙和尚', '沙悟净', '卷帘大将'],
    '如来': ['如来', '佛祖', '释迦牟尼', '释迦'],
    '观音': ['观音', '观音菩萨', '观世音', '观世音菩萨', '菩萨'],
    '玉帝': ['玉帝', '玉皇大帝', '天帝'],
    '白龙马': ['白龙马', '白马', '龙马'],
    '红孩儿': ['红孩儿', '圣婴大王'],
    '铁扇公主': ['铁扇公主', '罗刹女'],
    '牛魔王': ['牛魔王', '平天大圣'],
    '二郎神': ['二郎神', '二郎真君', '显圣二郎真君', '杨戬'],
    '太上老君': ['太上老君', '老君'],
    '弥勒佛': ['弥勒佛', '弥勒'],
    '唐王': ['唐王', '唐太宗', '李世民'],
    '黄袍怪': ['黄袍怪', '黄风怪'],
    '白骨精': ['白骨精', '白骨夫人'],
    '蜘蛛精': ['蜘蛛精', '七仙女'],
    '金角大王': ['金角大王', '金角'],
    '银角大王': ['银角大王', '银角'],
    '菩提祖师': ['菩提祖师', '菩提老祖', '须菩提祖师'],
    '黑熊精': ['黑熊精', '黑风怪'],
    '金鱼精': ['金鱼精', '龙女'],
    '六耳猕猴': ['六耳猕猴', '假悟空', '假孙悟空']
}

# 创建反向映射表，用于将别名映射回标准名称
# 例如: {'悟空': '孙悟空', '八戒': '猪八戒', ...}
name_mapping = {}
for standard, aliases in name_dict.items():
    for alias in aliases:
        name_mapping[alias] = standard

# 使用jieba进行分词处理
jieba.load_userdict(DICT_PATH)  # 加载自定义词典，提高分词准确率
words = jieba.lcut(content)  # 分词，返回词语列表

# 统计词频，使用Counter类计算每个词出现的次数
word_counts = collections.Counter(words)

# 过滤词频，去除单字和数字等，并合并人物别名
filtered_word_counts = {};
for word, count in word_counts.items():
    if len(word) >= 2 and not re.match(r'[0-9]+', word):  # 只保留长度>=2且不是纯数字的词
        # 检查是否是人物名
        if word in name_mapping:
            # 如果是人物名，将频次加到标准人物名下
            standard_name = name_mapping[word]
            if standard_name in filtered_word_counts:
                filtered_word_counts[standard_name] += count
            else:
                filtered_word_counts[standard_name] = count
        else:
            # 不是人物名直接添加到词频字典
            filtered_word_counts[word] = count

# 提取前24个人物，首先筛选出所有在词频表中出现的人物
characters = []
for name in name_dict.keys():
    if name in filtered_word_counts:
        characters.append((name, filtered_word_counts[name]))

# 按词频排序，取前24个
characters.sort(key=lambda x: x[1], reverse=True)
top_characters = characters[:24]
top_character_names = [char[0] for char in top_characters]  # 提取人物名列表

# 打印人物词频信息
print("\n前24名人物及其词频:")
for name, count in top_characters:
    print(f"{name}: {count}")

# 创建一个新的字典，专用于词云图，仅包含长度大于1且频次大于5的词
filtered_dict = {}
for word, count in filtered_word_counts.items():
    if len(word) > 1 and count > 5:  # 过滤掉单字和出现次数太少的词
        filtered_dict[word] = count

# 打印词频排名前20的词
print("\n词频前20的词:")
sorted_words = sorted(filtered_dict.items(), key=lambda x: x[1], reverse=True)
for word, count in sorted_words[:20]:
    print(f"{word}: {count}")

print(f"使用字体: {FONT_PATH}")

#————————————词云图设置————————————

# 词云形状选择交互界面
print("\n请选择词云图的形状:")
print("1. 矩形")
print("2. 圆形")
print("3. 猴子形状")
shape_choice = input("请输入选择(1-3), 默认为1: ").strip()

# 背景颜色选择交互界面
print("\n请选择词云图的背景颜色:")
print("1. 白色 (默认)")
print("2. 黑色")
print("3. 自定义颜色(自行输入)")
color_choice = input("请输入选择(1-3), 默认为1: ").strip()

# 颜色映射主题选择交互界面
print("\n请选择词云图的颜色主题:")
print("1. 默认")
print("2. 彩虹")
print("3. 红色系")
colormap_choice = input("请输入选择(1-3), 默认为1: ").strip()

# 根据用户选择设置词云形状
mask = None  # 用于控制词云形状

if shape_choice == '2':
    # 生成圆形蒙版
    x, y = np.ogrid[:800, :800]  # 创建网格坐标
    mask = ((x - 400) ** 2 + (y - 400) ** 2 > 400 ** 2) | ((x - 400) ** 2 + (y - 400) ** 2 < 50 ** 2)
    mask = 255 * np.ones((800, 800))  # 创建白色底板
    circle_mask = np.zeros((800, 800))  # 创建圆形蒙版
    center = (400, 400)  # 圆心坐标
    radius = 390  # 圆半径
    y, x = np.ogrid[:800, :800]  # 重新创建网格坐标
    circle_mask = ((x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2)  # 圆形区域
    mask[circle_mask] = 0  # 在圆形区域内设置为黑色
    print("已选择圆形词云")
elif shape_choice == '3':
    # 创建简化版猴子形状蒙版
    mask = np.zeros((800, 800), dtype=np.uint8)  # 创建黑色底板
    # 猴子头部 - 使用圆形表示
    center = (400, 350)
    radius = 200
    y, x = np.ogrid[:800, :800]
    head_mask = ((x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2)
    # 猴子耳朵 - 使用两个小圆表示
    ear1_center = (250, 200)
    ear1_radius = 80
    ear1_mask = ((x - ear1_center[0]) ** 2 + (y - ear1_center[1]) ** 2 <= ear1_radius ** 2)
    ear2_center = (550, 200)
    ear2_radius = 80
    ear2_mask = ((x - ear2_center[0]) ** 2 + (y - ear2_center[1]) ** 2 <= ear2_radius ** 2)
    # 合并所有部分形成猴子形状
    mask[head_mask | ear1_mask | ear2_mask] = 255  # 在相应区域设置为白色
    print("已选择猴子形状词云")
else:
    print("使用默认矩形词云")

# 设置背景颜色
bg_color = 'white'  # 默认白色背景
if color_choice == '2':
    bg_color = 'black'
elif color_choice == '3':
    bg_color_input = input("请输入自定义颜色(如red, #FF0000): ").strip()
    bg_color = bg_color_input if bg_color_input else 'white'
    print(f"已选择自定义背景色: {bg_color}")

# 设置颜色映射主题
colormap = None  # 默认无特定颜色映射
if colormap_choice == '2':
    colormap = 'rainbow'  # 彩虹色系
    print("已选择彩虹色主题")
elif colormap_choice == '3':
    colormap = 'Reds'  # 红色系
    print("已选择红色系主题")

#————————这一段是生成词云图————————

# 准备词云参数字典
wordcloud_params = {
    'font_path': FONT_PATH,  # 字体路径
    'background_color': bg_color,  # 背景颜色
    'max_words': 100,  # 最大显示词数
    'max_font_size': 150,  # 最大字体大小
    'width': 800,  # 宽度
    'height': 800 if shape_choice in ['2', '4', '5'] else 600,  # 高度，圆形和特殊形状使用正方形
    'random_state': 42,  # 随机种子，保证每次生成的词云位置相同
    'collocations': False,  # 不包含重复词语
    'prefer_horizontal': 0.9,  # 水平显示的概率
    'contour_width': 1,  # 轮廓宽度
    'contour_color': 'black' if bg_color != 'black' else 'white'  # 轮廓颜色
}

# 如果有蒙版，添加到参数中
if mask is not None:
    wordcloud_params['mask'] = mask

# 如果有颜色主题，添加到参数中
if colormap:
    wordcloud_params['colormap'] = colormap

# 生成词云对象
wordcloud = WordCloud(**wordcloud_params).generate_from_frequencies(filtered_dict)

# 创建图形对象并设置大小
plt.figure(figsize=(10, 10) if shape_choice in ['2', '4', '5'] else (10, 8))
plt.imshow(wordcloud, interpolation="bilinear")  # 显示词云图像
plt.axis("off")  # 不显示坐标轴

# 设置标题颜色，深色背景使用白色标题，浅色背景使用黑色标题
title_color = 'black' if bg_color in ['white', 'lightblue', 'lightyellow'] else 'white'
plt.title("西游记词云图", fontproperties=FontProperties(fname=FONT_PATH), color=title_color)

# 保存词云图到文件
plt.savefig(os.path.join(OUTPUT_DIR, "西游记词云图.png"), dpi=300, bbox_inches='tight', 
           facecolor=bg_color)
plt.close()  # 关闭图形

# 保存词云配置信息到文本文件，便于记录
with open(os.path.join(OUTPUT_DIR, "词云配置.txt"), "w", encoding="utf-8") as f:
    f.write(f"形状选择: {shape_choice}\n")
    f.write(f"背景颜色: {bg_color}\n")
    f.write(f"颜色主题: {colormap if colormap else '默认'}\n")

#————————接下来是人物关系处理——————————

# 分段处理文本，使用空行分割段落
paragraphs = re.split(r'\n+', content)
relationships = {}  # 存储人物关系的嵌套字典

# 初始化关系矩阵，为每对人物创建关系计数
for name1 in top_character_names:
    relationships[name1] = {}
    for name2 in top_character_names:
        relationships[name1][name2] = 0

# 遍历每个段落，统计人物共现关系
for paragraph in paragraphs:
    characters_in_para = set()  # 使用集合存储段落中出现的人物，避免重复
    
    # 检查段落中出现的人物
    for word in jieba.lcut(paragraph):
        if word in name_mapping and name_mapping[word] in top_character_names:
            characters_in_para.add(name_mapping[word])  # 添加标准人物名到集合
    
    # 如果段落中出现了多个人物，更新它们之间的共现关系
    characters_list = list(characters_in_para)
    for i in range(len(characters_list)):
        for j in range(i+1, len(characters_list)):
            # 为每对共同出现的人物增加关系权重
            relationships[characters_list[i]][characters_list[j]] += 1
            relationships[characters_list[j]][characters_list[i]] += 1  # 对称关系

#————————这一段是构建人物关系网络图————————

# 创建无向图对象
G = nx.Graph()

# 添加节点，每个节点代表一个人物，权重为词频
for name, count in top_characters:
    G.add_node(name, weight=count)

# 添加边，每条边代表两个人物之间的关系，权重为共现次数
for name1, related in relationships.items():
    for name2, weight in related.items():
        if weight > 0 and name1 != name2:  # 只添加有关系且不是自己与自己的关系
            G.add_edge(name1, name2, weight=weight)

# 设置节点大小，基于词频
node_sizes = [G.nodes[character]['weight'] * 5 for character in G.nodes]
max_node_size = max(node_sizes)
min_node_size = min(node_sizes)
# 缩放节点大小到范围(100-1000)，避免极大或极小节点(测试的时候出现了问题)
node_sizes = [100 + (ns - min_node_size) * 1000 / (max_node_size - min_node_size) for ns in node_sizes]

# 设置边的宽度，基于共现频率
edge_weights = [G[u][v]['weight'] * 0.2 for u, v in G.edges]
# 限制边的最大宽度，避免过粗的边
edge_weights = [min(w, 5) for w in edge_weights]

# 创建字体属性对象，用于中文显示
font_prop = FontProperties(fname=FONT_PATH)

# 绘制网络图
plt.figure(figsize=(16, 12))  # 创建大尺寸图形
pos = nx.kamada_kawai_layout(G)  # 使用Kamada-Kawai算法计算节点位置，减少节点重叠,这个确实一开始没想到

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.8)

# 绘制边
nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color="gray")

# 绘制标签，使用指定字体，并微调位置避免遮挡
labels = {node: node for node in G.nodes()}
for node, (x, y) in pos.items():
    plt.text(x, y+0.02, s=node, fontproperties=font_prop, ha='center', va='center', 
             fontsize=12, fontweight='bold')

# 添加标题
plt.title("西游记人物关系网络图", fontproperties=font_prop, fontsize=18)
plt.axis("on")  # 不显示坐标轴

# 保存网络图到文件
plt.savefig(os.path.join(OUTPUT_DIR, "西游记人物关系网络图.png"), dpi=300, bbox_inches='tight')
plt.close()  # 关闭图形

print("\n分析完成！图像已保存到output目录")
