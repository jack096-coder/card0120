from PIL import Image, ImageDraw, ImageFont
import json

class AnswerCardGenerator:
    def __init__(self):
        # 設定畫布大小 (寬, 高) 模擬 A4 比例
        self.width = 1240
        self.height = 1754
        self.img = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.img)
        
        # 資料記錄字典
        self.data = {
            "anchors": [],        # (1) 定位點座標
            "bubbles": [],        # (2) 劃記圓圈資訊
            "mixed_area": None    # (3) 非選區座標
        }
        
        # 字型設定 (若系統無預設字型，請更換路徑)
        try:
            self.font_sm = ImageFont.truetype("arial.ttf", 20)
            self.font_md = ImageFont.truetype("arial.ttf", 24)
        except:
            self.font_sm = ImageFont.load_default()
            self.font_md = ImageFont.load_default()

    def draw_anchors(self):
        """繪製四個角落的黑色定位方塊"""
        size = 40
        margin = 30
        positions = [
            (margin, margin),                                  # 左上
            (self.width - margin - size, margin),             # 右上
            (margin, self.height - margin - size),            # 左下
            (self.width - margin - size, self.height - margin - size) # 右下
        ]
        
        for pos in positions:
            x, y = pos
            box = [x, y, x + size, y + size]
            self.draw.rectangle(box, fill='black')
            # 記錄四個角座標
            self.data["anchors"].append([
                (x, y), (x + size, y), (x + size, y + size), (x, y + size)
            ])

    def draw_header(self):
        """繪製標題與個人資訊欄"""
        # 繪製主邊框與表格線
        self.draw.text((60, 80), "國立臺南大學附屬高級中學試卷答案卡", fill='black', font=self.font_md)
        self.draw.rectangle([60, 110, 550, 200], outline='black', width=2)
        self.draw.line([220, 110, 220, 200], fill='black', width=2)
        self.draw.line([400, 110, 400, 200], fill='black', width=2)
        self.draw.text((70, 130), "年   班      號  姓名：", fill='black', font=self.font_sm)
        self.draw.text((410, 130), "科目：", fill='black', font=self.font_sm)

    def draw_student_info_grid(self):
        """繪製班級座號劃記區"""
        start_x, start_y = 60, 230
        row_h = 40
        col_w = 40
        radius = 15

        # 標題欄
        labels = ["年級", "班十", "級個", "座十", "號個"]
        for i, label in enumerate(labels):
            curr_y = start_y + i * row_h
            self.draw.text((start_x, curr_y), label, fill='black', font=self.font_sm)
            
            # 繪製對應的圓圈
            num_range = range(1, 4) if i == 0 else range(0, 10)
            for j, num in enumerate(num_range):
                cx = start_x + 80 + j * col_w
                cy = curr_y + 12
                self._draw_bubble(cx, cy, radius, str(num))

    def draw_multiple_choice(self):
        """繪製 1-40 題多選題區"""
        base_x = 60
        base_y = 480
        col_spacing = 260
        row_spacing = 38
        radius = 15
        options = ['A', 'B', 'C', 'D', 'E']

        for i in range(40):
            col = i // 20
            row = i % 20
            x = base_x + col * col_spacing
            y = base_y + row * row_spacing
            
            # 題號
            self.draw.text((x, y), f"{i+1:02d}", fill='black', font=self.font_sm)
            
            # 選項圓圈
            for j, opt in enumerate(options):
                cx = x + 60 + j * 45
                cy = y + 12
                self._draw_bubble(cx, cy, radius, opt)

    def draw_mixed_area(self):
        """繪製右側非選擇題答案區"""
        box = [600, 110, 1100, 1600]
        self.draw.rectangle(box, outline='black', width=2)
        # 標題
        self.draw.rectangle([600, 110, 1100, 170], outline='black', width=2)
        self.draw.text((610, 130), "混合題（務必依序標示題號寫答案）", fill='black', font=self.font_sm)
        
        # 記錄四個角座標
        x1, y1, x2, y2 = box
        self.data["mixed_area"] = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    def _draw_bubble(self, cx, cy, r, label):
        """輔助函式：繪製圓圈並記錄資料"""
        self.draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline='black', width=1)
        self.draw.text((cx-6, cy-10), label, fill='black', font=self.font_sm)
        # 記錄 (2) 圓心與半徑
        self.data["bubbles"].append({"label": label, "center": (cx, cy), "radius": r})

    def save(self):
        # 存成圖片
        self.img.save("answer_card_redrawn.png")
        # 存成座標資料檔
        with open("coordinates.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print("答案卡已重繪完成，圖片存為 answer_card_redrawn.png，座標存為 coordinates.json")

if __name__ == "__main__":
    generator = AnswerCardGenerator()
    generator.draw_anchors()
    generator.draw_header()
    generator.draw_student_info_grid()
    generator.draw_multiple_choice()
    generator.draw_mixed_area()
    generator.save()
