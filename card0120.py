from PIL import Image, ImageDraw, ImageFont
import json
import os

class AnswerCardGenerator:
    def __init__(self):
        # 設定畫布大小 (寬, 高) 模擬 A4 比例
        self.width = 1240
        self.height = 1754
        self.img = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.img)
        
        self.data = {
            "anchors": [],
            "bubbles": [],
            "mixed_area": None
        }
        
        # 嘗試載入系統字型，若失敗則使用內建預設字型
        self.font_sm = self._get_font(20)
        self.font_md = self._get_font(28)

    def _get_font(self, size):
        # 嘗試常見的字型路徑 (Windows, Mac/Linux)
        font_paths = [
            "arial.ttf", 
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", # Linux 常見字型
            "C:\\Windows\\Fonts\\arial.txt"
        ]
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
        return ImageFont.load_default() # 萬不得已使用預設

    def draw_anchors(self):
        """繪製四個角落的黑色定位方塊"""
        size = 40
        margin = 30
        positions = [
            (margin, margin),
            (self.width - margin - size, margin),
            (margin, self.height - margin - size),
            (self.width - margin - size, self.height - margin - size)
        ]
        for pos in positions:
            x, y = pos
            box = [x, y, x + size, y + size]
            self.draw.rectangle(box, fill='black')
            self.data["anchors"].append([(x, y), (x + size, y), (x + size, y + size), (x, y + size)])

    def draw_header(self):
        """繪製標題與個人資訊欄"""
        self.draw.text((60, 80), "國立臺南大學附屬高級中學試卷答案卡", fill='black', font=self.font_md)
        self.draw.rectangle([60, 120, 550, 210], outline='black', width=2)
        self.draw.line([220, 120, 220, 210], fill='black', width=2)
        self.draw.line([400, 120, 400, 210], fill='black', width=2)
        self.draw.text((70, 145), "年   班   號 姓名：", fill='black', font=self.font_sm)
        self.draw.text((410, 145), "科目：", fill='black', font=self.font_sm)

    def draw_student_info_grid(self):
        """繪製班級座號劃記區"""
        start_x, start_y = 60, 240
        row_h = 45
        col_w = 42
        radius = 16
        labels = ["年級", "班十", "級個", "座十", "號個"]
        for i, label in enumerate(labels):
            curr_y = start_y + i * row_h
            self.draw.text((start_x, curr_y), label, fill='black', font=self.font_sm)
            num_range = range(1, 4) if i == 0 else range(0, 10)
            for j, num in enumerate(num_range):
                cx = start_x + 90 + j * col_w
                cy = curr_y + 12
                self._draw_bubble(cx, cy, radius, str(num))

    def draw_multiple_choice(self):
        """繪製 1-40 題多選題區"""
        base_x, base_y = 60, 500
        col_spacing, row_spacing = 270, 42
        radius = 16
        options = ['A', 'B', 'C', 'D', 'E']
        for i in range(40):
            col, row = i // 20, i % 20
            x, y = base_x + col * col_spacing, base_y + row * row_spacing
            self.draw.text((x, y), f"{i+1:02d}", fill='black', font=self.font_sm)
            for j, opt in enumerate(options):
                cx, cy = x + 65 + j * 45, y + 12
                self._draw_bubble(cx, cy, radius, opt)

    def draw_mixed_area(self):
        """繪製右側非選擇題答案區"""
        box = [620, 120, 1150, 1680]
        self.draw.rectangle(box, outline='black', width=2)
        self.draw.rectangle([620, 120, 1150, 180], outline='black', width=2)
        self.draw.text((630, 140), "混合題（務必依序標示題號寫答案）", fill='black', font=self.font_sm)
        x1, y1, x2, y2 = box
        self.data["mixed_area"] = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    def _draw_bubble(self, cx, cy, r, label):
        self.draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline='black', width=1)
        # 修正文字置中位移
        self.draw.text((cx-6, cy-10), label, fill='black', font=self.font_sm)
        self.data["bubbles"].append({"label": label, "center": (cx, cy), "radius": r})

    def save(self):
        self.img.save("answer_card_redrawn.png")
        with open("coordinates.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print("Success: answer_card_redrawn.png and coordinates.json generated.")

if __name__ == "__main__":
    gen = AnswerCardGenerator()
    gen.draw_anchors()
    gen.draw_header()
    gen.draw_student_info_grid()
    gen.draw_multiple_choice()
    gen.draw_mixed_area()
    gen.save()
