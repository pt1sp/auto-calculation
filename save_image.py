import base64
from obswebsocket import requests
from io import BytesIO
from PIL import Image
import easyocr
from process_image import check_image_for_text
import tempfile
import time

reader = easyocr.Reader(['en'])

def save_image_from_obs(ws, image_file_path, capture_source, area=None):

    success = False

    response = ws.call(requests.GetSourceScreenshot(sourceName=capture_source, imageFormat="png", imageWidth=1920, imageHeight=1080))

    img_data_base64 = response.datain.get('imageData', None)
    if img_data_base64 is None:
        raise KeyError("スクリーンショットデータがレスポンスに含まれていません")

    if img_data_base64.startswith('data:image/png;base64,'):
        img_data_base64 = img_data_base64.split(',')[1]

    padding_needed = 4 - len(img_data_base64) % 4
    if padding_needed != 4:
        img_data_base64 += '=' * padding_needed

    img_data = base64.b64decode(img_data_base64)

    with BytesIO(img_data) as img_bytes:
        with Image.open(img_bytes) as img:
            img.save(image_file_path)
            if area:
                img = img.crop(area)
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    cropped_image_path = tmp.name
                    img.save(cropped_image_path)
                success = True

    if success:
        result = reader.readtext(cropped_image_path)
        results = [item[1] for item in result]
        results.append("0")
        if results[0] == '12':
            return check_image_for_text(image_file_path)
        else:
            time.sleep(1)
            return save_image_from_obs(ws, image_file_path, capture_source, area)