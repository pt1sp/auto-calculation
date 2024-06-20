import easyocr
from PIL import Image
import cv2
import numpy as np
import os

def preprocess_image(image_file_path, area):
    img = Image.open(image_file_path)
    cropped_img = img.crop(area)
    cropped_img.save("crop.png")

    # OpenCVを使用して画像を読み込み
    cv_img = cv2.imread("crop.png", cv2.IMREAD_GRAYSCALE)

    # ノイズ除去
    denoised = cv2.fastNlMeansDenoising(cv_img, h=30)

    # コントラスト調整
    alpha = 1.5  # コントラスト制御（1.0-3.0）
    beta = 0    # 明るさ制御（0-100）
    adjusted = cv2.convertScaleAbs(denoised, alpha=alpha, beta=beta)

    # 二値化
    _, binary = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 保存ディレクトリを指定
    save_dir = "processed_images"
    os.makedirs(save_dir, exist_ok=True)  # フォルダが存在しない場合は作成

    # フルパスを指定
    save_path = os.path.join(save_dir, "processed_crop.png")
    cv2.imwrite(save_path, binary)

    return save_path

def check_image_for_text(image_file_path):
    area = (1008, 80, 1300, 1000)
    point = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    text_groups = {}
    reader = easyocr.Reader(['en'], gpu=True)

    processed_img_path = preprocess_image(image_file_path, area)
    result = reader.readtext(processed_img_path)
    results = [item[1] for item in result]
    print(results)
    
    if len(results) != 12:
        print("人数が12ではありません")
        results = input().split()  # ユーザー入力をリストに分割
        results = [item.strip() for item in results]
        
    
    for i, text in enumerate(results):
        score = point[i] if i < len(point) else 0
        key = text[0] if len(text) == 1 else text[0]
        if key in text_groups:
            text_groups[key].append(score)
        else:
            text_groups[key] = [score]
    
    group_scores = {key: sum(scores) for key, scores in text_groups.items()}
     
    teams = list(group_scores.keys())
    scores = [group_scores[key] for key in teams]

    return teams, scores
