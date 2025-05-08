import os,io,requests,re
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

#——————————添加水印——————————
def add_watermark(img_bytes: bytes, text: str, pos: int = 4) -> bytes:

    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)

    fsize = max(12, int(img.width * 0.035))
    try:
        font_path = os.path.join(os.path.dirname(__file__), "data/SourceHanSansHWSC-Regular.otf")   #用data里的思源黑体
        font = ImageFont.truetype(font_path, fsize)
    except OSError:
        font = ImageFont.load_default()

    # Pillow ≥10 用 textbbox 计算文字尺寸
    # 返回 (x0, y0, x1, y1)
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pos_tbl = {
        1: (10, 10),
        2: (10, img.height - h - 10),
        3: (img.width - w - 10, 10),
        4: (img.width - w - 10, img.height - h - 10)
    }
    draw.text(pos_tbl[pos], text, fill=(255, 255, 255, 160), font=font)
    img = img.convert("RGB")
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=95)
    return out.getvalue()



#————————————下载程序——————————
def download(keyword,pn,startid,pos):
    #————————参数————————
    url =f"https://image.baidu.com/search/index?word={keyword}&pn={pn}"     #百度下载地址
    ua ={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'Referer':'https://image.baidu.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }                                                                            #定义ua
    resp = requests.get(url,headers=ua)                                              #发送请求
    water_txt = "网安2301 刘毅凡 34"                                                   #水印参数
    save_dir = os.path.join(os.path.expanduser("~/Downloads/len5010"), keyword)      #默认下载路径
    os.makedirs(save_dir, exist_ok=True)                                             #没有就自动创建

    #——————————抓url——————————
    html_txt = resp.text          #获取的内容
    img_urls = []                 #匹配的目标图片url
    print(f"第{pn+1}页访问状态:{resp.status_code}")        #查看请求的状态 
    html_soup = BeautifulSoup(html_txt, 'html.parser')
    html_sc = html_soup.find_all('script',string=re.compile(r'"objurl":'))  #使用bs查找包含objurl的字段
    for html_txt in html_sc:
        html_target = html_txt.string      #指向的target
        if not html_target:
            continue                       #没有url
        url_target = r'"objurl":"(https?://[^"&]+?\.jpg)"'  #限定.jpg 结尾，排除非法字符
        matches = re.findall(url_target, html_target)
        if matches:
            img_urls.extend(matches)    #在总的html文本里面匹配需要的字段
        if not img_urls:
            print("没有找到图片")
        else:
            print(f"成功匹配 {len(img_urls)} 条 .jpg 链接：")   

    #-————下载并加水印
    good, bad = 0, 0
    for i, link in enumerate(img_urls, 1):
        try:
            r = requests.get(link, headers=ua, timeout=10)
            r.raise_for_status()
            # 加水印
            wm_img = add_watermark(r.content, water_txt, pos)
            # 文件名
            idx   = startid + i            
            fname = os.path.join(save_dir, f"刘毅凡{idx}.jpg")
            with open(fname, 'wb') as f:
                f.write(wm_img)
            good += 1
            print(f"[{good}/{len(img_urls)}] 已保存 {fname}")
        except Exception as e:
            bad += 1
            print(f"× 下载失败({bad})：{link} -> {e}")

    print(f"完成！成功 {good} 张，失败 {bad} 张，文件在 {save_dir}/")
    return good


#——————————主进程————————————
keyword = input("请输入关键词(请输入遐蝶💢)：").strip()
pages   = int(input("请输入要下载的页数："))       
pos  = int(input("请输入水印位置："))        

seq = 0                                    
for page in range(pages):                                 
    got = download(keyword, page, seq,pos)        
    seq += got                    

print("全部页面处理完毕")