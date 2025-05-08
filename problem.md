```python
def add_watermark(img_bytes: bytes, text: str, pos: int = 4) -> bytes:
#参数 pos：1~4 代表四个角，缺省 4=右下
#返回：加过水印的图片二进制


img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
draw = ImageDraw.Draw(img)
# 字体大小按图片宽度的 5% 来算
fsize = max(12, int(img.width * 0.05))
font = ImageFont.truetype("arial.ttf", fsize)
w, h = draw.textsize(text, font)

# 四个角坐标
pos_tbl = {
    1: (10, 10),
    2: (10, img.height - h - 10),
    3: (img.width - w - 10, 10),
    4: (img.width - w - 10, img.height - h - 10)
}
draw.text(pos_tbl[pos], text, fill=(255, 255, 255, 160), font=font)  # 160=半透明
out = io.BytesIO()
img.save(out, format="JPEG")
return out.getvalue()
```

Pillow 10.0 起彻底移除了 ImageDraw.textsize()。
所以在新版本里调用会直接抛出：

'ImageDraw' object has no attribute 'textsize'
只要把取文字宽高的方式改成官方推荐的新接口 (textbbox / Font.getsize) 就能一次性解决 33 张全部失败的问题。

