import easyocr
from PIL import Image
import cv2
import numpy as np
import os

def preprocess_image(image_file_path):
    img = Image.open(image_file_path)

    # OpenCVを使用して画像を読み込み
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # ノイズ除去
    denoised = cv2.fastNlMeansDenoising(cv_img, h=30)

    # コントラスト調整
    alpha = 1.5  # コントラスト制御（1.0-3.0）
    beta = 0    # 明るさ制御（0-100）
    adjusted = cv2.convertScaleAbs(denoised, alpha=alpha, beta=beta)

    # カラー画像をグレースケールに変換
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

    # 二値化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 保存ディレクトリを指定
    save_dir = "images"
    os.makedirs(save_dir, exist_ok=True)  # フォルダが存在しない場合は作成

    # フルパスを指定
    save_path = os.path.join(save_dir, "processed_image.png")
    cv2.imwrite(save_path, binary)

    return save_path

def check_image_for_text(image_file_path):
    areas = [
        (1015, 88, 1052, 140),
        (1015, 165, 1052, 215),
        (1015, 250, 1052, 288),
        (1015, 325, 1052, 367),
        (1015, 405, 1052, 447),
        (1015, 475, 1052, 527),
        (1015, 555, 1052, 605),
        (1015, 630, 1052, 685),
        (1015, 710, 1052, 765),
        (1015, 785, 1052, 845),
        (1015, 865, 1052, 920),
        (1015, 950, 1052, 990)
    ]
    point = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    text_groups = {}
    reader = easyocr.Reader(['en'], gpu=True)

    # 画像の処理を最初に実行
    processed_img_path = preprocess_image(image_file_path)

    # 画像をOpenCVで読み込み
    img = cv2.imread(processed_img_path)

    all_results = []
    for i, area in enumerate(areas):
        # 指定された領域を切り取る
        cropped_img = img[area[1]:area[3], area[0]:area[2]]
        crop_path = f"images/crop_{i+1}.png"
        cv2.imwrite(crop_path, cropped_img)

        # EasyOCRでテキストを読み取る
        result = reader.readtext(crop_path)
        results = [item[1] for item in result]
        print(results)
        all_results.append(results)

    # 結果が12個でない場合はユーザー入力で補正
    if len(all_results) != 12:
        print("人数が12ではありません")
        all_results = [input().split() for _ in range(12)]  # 各領域の結果をユーザー入力で補正
        all_results = [[item.strip() for item in results] for results in all_results]
    
    # 結果を集計
    for i, results in enumerate(all_results):
        if results:  # 結果が空でない場合のみ処理
            text = results[0]  # 最初のテキスト（1文字目）を取得
            key = text[0]  # チームのキーとして最初の文字を取得
            score = point[i] if i < len(point) else 0  # スコアを計算

            # スコアをグループに追加
            if key in text_groups:
                text_groups[key].append(score)
            else:
                text_groups[key] = [score]

    
    group_scores = {key: sum(scores) for key, scores in text_groups.items()}
    
    teams = list(group_scores.keys())
    scores = [group_scores[key] for key in teams]

    return teams, scores
