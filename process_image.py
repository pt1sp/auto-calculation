import easyocr
from PIL import Image

reader = easyocr.Reader(['en'])

def check_image_for_text(image_file_path):
    # ↓名前の部分の座標
    area = (1010, 80, 1300, 1000)
    point = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    text_groups = {}

    img = Image.open(image_file_path)
    cropped_img = img.crop(area)
    cropped_img.save("crop.png")
    result = reader.readtext("crop.png")
    results = [item[1] for item in result]
    print(results)
    
    if len(results) != 12:
        print("人数が12ではありません")
        results = input()
        results = [item[1] for item in result]
        
    
    for i, text in enumerate(results):
        score = point[i] if i < len(point) else 0
        key = text[0] if len(text) == 1 else (text[0])
        if key in text_groups:
            text_groups[key].append(score)
        else:
            text_groups[key] = [score]
    
    group_scores = {key: sum(scores) for key, scores in text_groups.items()}
     
    teams = list(group_scores.keys())
    scores = [group_scores[key] for key in teams]

    return teams, scores