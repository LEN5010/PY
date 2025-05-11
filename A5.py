import os
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
from PIL import Image, ImageDraw
from matplotlib.font_manager import FontProperties

# 设置文件路径,这里改成os.path.join,这样其他系统也可以运行
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, 'data', 'A5_picture')  # 读取图片A5_picture
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'A5_result')  # 输出目录设置data/A5_result
os.makedirs(DATA_DIR, exist_ok=True)  # 确保数据目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def lsb_encode(cover_image_path, secret_image_path, output_path):
    #cover_image_path载体图像的路径（用于隐藏信息的图像）
    #secret_image_path秘密图像的路径（要被隐藏的图像）
    #output_path输出隐写结果的路径
    
    # 打开载体图像和秘密图像
    cover_img = Image.open(cover_image_path).convert('RGB')
    secret_img = Image.open(secret_image_path).convert('RGB')
    
    # 调整秘密图像大小以匹配载体图像
    secret_img = secret_img.resize(cover_img.size)
    
    # 获取图像数据
    cover_data = np.array(cover_img)
    secret_data = np.array(secret_img)
    
    # 创建输出图像数组
    output_data = cover_data.copy()
    
    # 对每个像素进行LSB隐写
    for i in range(cover_data.shape[0]):
        for j in range(cover_data.shape[1]):
            for k in range(3):  # RGB通道
                # 清除载体图像像素的最低有效位
                output_data[i, j, k] = cover_data[i, j, k] & 0xFE
                
                # 获取秘密图像像素的最高有效位
                secret_bit = (secret_data[i, j, k] & 0x80) >> 7
                
                # 将秘密位嵌入到载体像素的最低有效位
                output_data[i, j, k] = output_data[i, j, k] | secret_bit
    
    # 创建并保存隐写后的图像
    output_img = Image.fromarray(output_data.astype(np.uint8))
    output_img.save(output_path)
    print(f"隐写完成！结果已保存到: {output_path}")

def lsb_decode(stego_image_path, output_path):
    
    #stego_image_path: 包含隐藏信息的图像路径
    #output_path: 提取出的秘密图像的保存路径

    # 打开包含隐藏信息的图像
    stego_img = Image.open(stego_image_path).convert('RGB')
    stego_data = np.array(stego_img)
    
    # 创建输出图像数组
    output_data = np.zeros_like(stego_data)
    
    # 对每个像素进行LSB提取
    for i in range(stego_data.shape[0]):
        for j in range(stego_data.shape[1]):
            for k in range(3):  # RGB通道
                # 获取载体图像像素的最低有效位
                secret_bit = stego_data[i, j, k] & 0x01
                
                # 将提取的位放入输出图像的最高有效位
                output_data[i, j, k] = secret_bit << 7
    
    # 创建并保存提取的秘密图像
    output_img = Image.fromarray(output_data.astype(np.uint8))
    output_img.save(output_path)
    print(f"提取完成！秘密图像已保存到: {output_path}")

def list_images(directory):
    # 列出目录中所有图片文件
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
    image_files = []
    
    try:
        # 获取目录中的所有文件
        files = os.listdir(directory)
        
        # 筛选出图片文件
        for file in files:
            # 获取文件扩展名
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                image_files.append(file)
                
        return image_files
    except Exception as e:
        print(f"列出图片文件时出错: {e}")
        return []

def select_image(directory, prompt):
    # 从目录中选择一个图片文件
    images = list_images(directory)
    
    if not images:
        print(f"目录 {directory} 中没有找到图片文件")
        return None
    
    print(f"\n{prompt}")
    print("可用的图片文件:")
    
    # 显示可用图片文件列表
    for i, image in enumerate(images, start=1):
        print(f"{i}. {image}")
    
    # 获取用户选择
    while True:
        try:
            choice = int(input("\n请输入图片序号 (0 退出): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(images):
                return os.path.join(directory, images[choice-1])
            else:
                print(f"请输入1-{len(images)}之间的数字")
        except ValueError:
            print("请输入有效的数字")

def main():
    #主函数 - 交互式选择图片进行隐写和提取
    
    while True:
        print("\n——————LSB图片隐写程序——————")
        print("1. 执行图片隐写")
        print("2. 从隐写图片中提取秘密图像")
        print("0. 退出程序")
        
        choice = input("\n请选择操作: ")
        
        if choice == "1":
            # 隐写操作
            print("\n——————执行图片隐写——————")
            
            # 选择载体图像
            cover_image = select_image(DATA_DIR, "请选择载体图像 (用来隐藏信息的图像):")
            if not cover_image:
                print("未选择载体图像，返回主菜单")
                continue
                
            # 选择秘密图像
            secret_image = select_image(DATA_DIR, "请选择秘密图像 (要被隐藏的图像):")
            if not secret_image:
                print("未选择秘密图像，返回主菜单")
                continue
            
            # 设置输出文件名
            output_filename = input("请输入输出文件名 (如 result.png): ")
            if not output_filename:
                output_filename = "stego_image.png"
                
            # 添加扩展名如果没有的话
            if not any(output_filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']):
                output_filename += ".png"
                
            stego_image = os.path.join(OUTPUT_DIR, output_filename)
            
            # 执行LSB隐写
            try:
                lsb_encode(cover_image, secret_image, stego_image)
                print(f"隐写操作完成，结果保存到: {stego_image}")
            except Exception as e:
                print(f"隐写过程中出错: {e}")
            
        elif choice == "2":
            # 提取操作
            print("\n——————从隐写图片提取秘密图像——————")
            
            # 选择要提取的隐写图像
            stego_image = select_image(OUTPUT_DIR, "请选择包含隐藏信息的图像:")
            if not stego_image:
                print("未选择隐写图像，返回主菜单")
                continue
                
            # 设置输出文件名
            output_filename = input("请输入提取结果的文件名 (不包含路径，例如 'extracted.png'): ")
            if not output_filename:
                output_filename = "extracted_secret.png"
                
            # 添加扩展名如果没有的话
            if not any(output_filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']):
                output_filename += ".png"
                
            extracted_image = os.path.join(OUTPUT_DIR, output_filename)
            
            # 执行提取
            try:
                lsb_decode(stego_image, extracted_image)
                print(f"提取操作完成，结果保存到: {extracted_image}")
            except Exception as e:
                print(f"提取过程中出错: {e}")
            
        elif choice == "0":
            # 退出程序
            print("程序已退出")
            break
            
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main()