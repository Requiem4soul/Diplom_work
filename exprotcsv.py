import csv
import json
from io import StringIO

data = """frame_0.jpg,477843,"{}",54,0,"{""name"":""rect"",""x"":312,""y"":184,""width"":52,""height"":97}","{}"
frame_0.jpg,477843,"{}",54,1,"{""name"":""rect"",""x"":378,""y"":197,""width"":81,""height"":33}","{}"
frame_0.jpg,477843,"{}",54,2,"{""name"":""rect"",""x"":141,""y"":344,""width"":74,""height"":43}","{}"
frame_0.jpg,477843,"{}",54,3,"{""name"":""rect"",""x"":116,""y"":425,""width"":57,""height"":39}","{}"
frame_0.jpg,477843,"{}",54,4,"{""name"":""rect"",""x"":367,""y"":265,""width"":69,""height"":18}","{}"
frame_0.jpg,477843,"{}",54,5,"{""name"":""rect"",""x"":344,""y"":321,""width"":67,""height"":18}","{}"
frame_0.jpg,477843,"{}",54,6,"{""name"":""rect"",""x"":332,""y"":371,""width"":60,""height"":17}","{}"
frame_0.jpg,477843,"{}",54,7,"{""name"":""rect"",""x"":304,""y"":420,""width"":66,""height"":14}","{}"
frame_0.jpg,477843,"{}",54,8,"{""name"":""rect"",""x"":281,""y"":467,""width"":74,""height"":24}","{}"
frame_0.jpg,477843,"{}",54,9,"{""name"":""rect"",""x"":253,""y"":517,""width"":61,""height"":29}","{}"
frame_0.jpg,477843,"{}",54,10,"{""name"":""rect"",""x"":244,""y"":569,""width"":52,""height"":24}","{}"
frame_0.jpg,477843,"{}",54,11,"{""name"":""rect"",""x"":200,""y"":633,""width"":75,""height"":29}","{}"
frame_0.jpg,477843,"{}",54,12,"{""name"":""rect"",""x"":157,""y"":710,""width"":22,""height"":67}","{}"
frame_0.jpg,477843,"{}",54,13,"{""name"":""rect"",""x"":143,""y"":993,""width"":89,""height"":32}","{}"
frame_0.jpg,477843,"{}",54,14,"{""name"":""rect"",""x"":297,""y"":993,""width"":97,""height"":33}","{}"
frame_0.jpg,477843,"{}",54,15,"{""name"":""rect"",""x"":449,""y"":996,""width"":98,""height"":34}","{}"
frame_0.jpg,477843,"{}",54,16,"{""name"":""rect"",""x"":646,""y"":1002,""width"":107,""height"":41}","{}"
frame_0.jpg,477843,"{}",54,17,"{""name"":""rect"",""x"":826,""y"":999,""width"":93,""height"":43}","{}"
frame_0.jpg,477843,"{}",54,18,"{""name"":""rect"",""x"":988,""y"":1012,""width"":130,""height"":50}","{}"
frame_0.jpg,477843,"{}",54,19,"{""name"":""rect"",""x"":562,""y"":926,""width"":104,""height"":39}","{}"
frame_0.jpg,477843,"{}",54,20,"{""name"":""rect"",""x"":219,""y"":700,""width"":32,""height"":73}","{}"
frame_0.jpg,477843,"{}",54,21,"{""name"":""rect"",""x"":278,""y"":698,""width"":32,""height"":88}","{}"
frame_0.jpg,477843,"{}",54,22,"{""name"":""rect"",""x"":334,""y"":702,""width"":42,""height"":81}","{}"
frame_0.jpg,477843,"{}",54,23,"{""name"":""rect"",""x"":405,""y"":708,""width"":32,""height"":84}","{}"
frame_0.jpg,477843,"{}",54,24,"{""name"":""rect"",""x"":477,""y"":696,""width"":36,""height"":89}","{}"
frame_0.jpg,477843,"{}",54,25,"{""name"":""rect"",""x"":541,""y"":714,""width"":37,""height"":76}","{}"
frame_0.jpg,477843,"{}",54,26,"{""name"":""rect"",""x"":614,""y"":719,""width"":31,""height"":74}","{}"
frame_0.jpg,477843,"{}",54,27,"{""name"":""rect"",""x"":684,""y"":713,""width"":27,""height"":73}","{}"
frame_0.jpg,477843,"{}",54,28,"{""name"":""rect"",""x"":816,""y"":604,""width"":81,""height"":29}","{}"
frame_0.jpg,477843,"{}",54,29,"{""name"":""rect"",""x"":917,""y"":704,""width"":25,""height"":84}","{}"
frame_0.jpg,477843,"{}",54,30,"{""name"":""rect"",""x"":1040,""y"":424,""width"":22,""height"":65}","{}"
frame_0.jpg,477843,"{}",54,31,"{""name"":""rect"",""x"":1175,""y"":463,""width"":88,""height"":27}","{}"
frame_0.jpg,477843,"{}",54,32,"{""name"":""rect"",""x"":1165,""y"":518,""width"":93,""height"":34}","{}"
frame_0.jpg,477843,"{}",54,33,"{""name"":""rect"",""x"":1129,""y"":582,""width"":98,""height"":36}","{}"
frame_0.jpg,477843,"{}",54,34,"{""name"":""rect"",""x"":1112,""y"":646,""width"":79,""height"":28}","{}"
frame_0.jpg,477843,"{}",54,35,"{""name"":""rect"",""x"":1128,""y"":770,""width"":24,""height"":83}","{}"
frame_0.jpg,477843,"{}",54,36,"{""name"":""rect"",""x"":1199,""y"":1021,""width"":102,""height"":34}","{}"
frame_0.jpg,477843,"{}",54,37,"{""name"":""rect"",""x"":1301,""y"":746,""width"":39,""height"":94}","{}"
frame_0.jpg,477843,"{}",54,38,"{""name"":""rect"",""x"":1389,""y"":737,""width"":52,""height"":88}","{}"
frame_0.jpg,477843,"{}",54,39,"{""name"":""rect"",""x"":1397,""y"":1031,""width"":120,""height"":27}","{}"
frame_0.jpg,477843,"{}",54,40,"{""name"":""rect"",""x"":1588,""y"":919,""width"":103,""height"":106}","{}"
frame_0.jpg,477843,"{}",54,41,"{""name"":""rect"",""x"":1705,""y"":803,""width"":97,""height"":104}","{}"
frame_0.jpg,477843,"{}",54,42,"{""name"":""rect"",""x"":1826,""y"":686,""width"":80,""height"":98}","{}"
frame_0.jpg,477843,"{}",54,43,"{""name"":""rect"",""x"":1509,""y"":653,""width"":112,""height"":115}","{}"
frame_0.jpg,477843,"{}",54,44,"{""name"":""rect"",""x"":1681,""y"":545,""width"":89,""height"":50}","{}"
frame_0.jpg,477843,"{}",54,45,"{""name"":""rect"",""x"":1712,""y"":444,""width"":79,""height"":31}","{}"
frame_0.jpg,477843,"{}",54,46,"{""name"":""rect"",""x"":1665,""y"":378,""width"":99,""height"":31}","{}"
frame_0.jpg,477843,"{}",54,47,"{""name"":""rect"",""x"":1658,""y"":331,""width"":90,""height"":25}","{}"
frame_0.jpg,477843,"{}",54,48,"{""name"":""rect"",""x"":1632,""y"":281,""width"":81,""height"":28}","{}"
frame_0.jpg,477843,"{}",54,49,"{""name"":""rect"",""x"":1642,""y"":218,""width"":81,""height"":37}","{}"
frame_0.jpg,477843,"{}",54,50,"{""name"":""rect"",""x"":1850,""y"":247,""width"":59,""height"":76}","{}"
frame_0.jpg,477843,"{}",54,51,"{""name"":""rect"",""x"":1814,""y"":160,""width"":46,""height"":60}","{}"
frame_0.jpg,477843,"{}",54,52,"{""name"":""rect"",""x"":1781,""y"":76,""width"":36,""height"":55}","{}"
frame_0.jpg,477843,"{}",54,53,"{""name"":""rect"",""x"":1784,""y"":10,""width"":36,""height"":34}","{}"""

# Используем csv.reader для чтения данных, учитывая, что разделителем является ","
reader = csv.reader(StringIO(data))

# Извлекаем значения x, y, width, height из каждой строки
parking_spots = []
for row in reader:
    _, _, _, _, _, rect_str, _ = row
    rect_data = json.loads(rect_str)
    x, y, width, height = rect_data["x"], rect_data["y"], rect_data["width"], rect_data["height"]
    parking_spots.append((x, y, width, height))

# Выведем результат
print("parking_spots =", parking_spots)
