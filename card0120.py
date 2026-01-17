import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io

class AnswerCardGenerator:
    def __init__(self):
        self.width = 1240
        self.height = 1754
        self.img = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.img)
        self.data = {"anchors": [], "bubbles": [], "mixed_area": None}
        self.font_sm = self._get_font(20)
        self.font_md = self._get_font(28)

    def _get_font(self, size):
        # 優先嘗試載入系統常見字型，失敗則用預設
        font_paths = ["arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
        for path in font_paths:
            try: return ImageFont.truetype(path, size)
            except: continue
        return ImageFont.load_default()

    def draw_anchors(self):
        size, margin = 40, 30
        positions = [(margin, margin), (self.width-margin-size, margin),
                     (margin, self.height-margin-size), (self.width-margin-size, self.height-margin-size)]
        for x, y in positions:
            self.draw.rectangle([x, y, x+size, y+size], fill='black')
            self.data["anchors"].append([(x, y), (x+size, y), (x+size, y+size), (x, y+size)])

    def draw_header(self):
        self.draw.text((60, 80), "國立臺南大學附屬高級中學試卷答案卡", fill='black', font=self.font_md)
        self.draw.rectangle([60, 120, 550, 210], outline='black', width=2)
        self.draw.line([220, 120, 220, 210], fill='black', width=2)
        self.draw.line([400, 120, 400, 210], fill='black', width=2)
        self.draw.text((70, 145), "年   班   號 姓名：", fill='black', font=self.font_sm)
        self.draw.text((410, 145), "科目：", fill='black', font=self.font_sm)

    def draw_student_info(self):
        start_x, start_y = 60, 240
        row_h, col_w, r = 45, 42, 16
        labels = ["年級", "班十", "級個", "座十", "號個"]
        for i, label in enumerate(labels):
            y = start_y + i * row_h
            self.draw.text((start_x, y), label, fill='black', font=self.font_sm)
            nums = range(1, 4) if i == 0 else range(0, 10)
            for j, num in enumerate(nums):
                cx, cy = start_x + 90 + j * col_w, y + 12
                self._draw_bubble(cx, cy, r, str(num))

    def draw_multiple_choice(self):
        base_x, base_y = 60, 500
        row_s, col_s, r = 42, 270, 16
        for i in range(40):
            col, row = i // 20, i % 20
            x, y = base_x + col * col_s, base_y + row * row_s
            self.draw.text((x, y), f"{i+1:02d}", fill='black', font=self.font_sm)
            for j, opt in enumerate(['A', 'B', 'C', 'D', 'E']):
                cx, cy = x + 65 + j * 45, y + 12
                self._draw_bubble(cx, cy, r, opt)

    def draw_mixed_area(self):
        box = [620, 120, 1150, 1680]
        self.draw.rectangle(box, outline='black', width=2)
        self.draw.rectangle([620, 120, 1150, 180], outline='black', width=2)
        self.draw.text((630, 140), "混合題（務必依序標示題號寫答案）", fill='black', font=self.font_sm)
        self.data["mixed_area"] = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]

    def _draw_bubble(self, cx, cy, r, label):
        self.draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline='black', width=1)
        self.draw.text((cx-6, cy-10), label, fill='black', font=self.font_sm)
        self.data["bubbles"].append({"label": label, "center": (cx, cy), "radius": r})

# Streamlit 網頁呈現
st.title("答案卡自動生成器")

if st.button("點擊生成答案卡"):
    gen = AnswerCardGenerator()
    gen.draw_anchors()
    gen.draw_header()
    gen.draw_student_info()
    gen.draw_multiple_choice()
    gen.draw_mixed_area()
    
    # 顯示圖片
    st.image(gen.img, caption="生成的答案卡預覽", use_container_width=True)
    
    # 下載圖片
    buf = io.BytesIO()
    gen.img.save(buf, format="PNG")
    st.download_button("下載圖片 (PNG)", buf.getvalue(), "answer_card.png", "image/png")
    
    # 下載座標 JSON
    json_str = json.dumps(gen.data, indent=4, ensure_ascii=False)
    st.download_button("下載座標資料 (JSON)", json_str, "coordinates.json", "application/json")
