from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
import json
from typing import Optional
from pydantic import BaseModel
import glob
import os
#import torch
#torch.cuda.is_available = lambda : False  # принудительно использовать только CPU для PyTorch

app = FastAPI()  # Инициализация FastAPI

default_mdl_path = './models/'  # Путь по умолчанию, где хранятся модели

def get_latest_model(path):  # Функция для выбора самой последней модели
    list_of_files = glob.glob(f'{path}*.pt')
    if not list_of_files:
        return None  # Ни одного файла модели не найдено
    return max(list_of_files, key=os.path.getctime)  # Выбираем самый свежий файл

@app.post("/predict/")
async def predict(file: UploadFile = File(...), mdl_name: Optional[str] = Form(None)):
    image_stream = io.BytesIO(await file.read())
    image_stream.seek(0)
    image = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), 1)
    image_stream.close()

    if image is None:
        return {"error": "Invalid image file"}

    # Если имя модели предоставлено, создаем полный путь к модели
    if mdl_name:
        selected_model = os.path.join(default_mdl_path, mdl_name)
        # Проверяем, существует ли файл модели
        if not os.path.exists(selected_model):
            selected_model = get_latest_model(default_mdl_path)
    else:
        selected_model = get_latest_model(default_mdl_path)

    if selected_model is None:
        return {"error": "No model files found"}

    model = YOLO(selected_model)  # Assuming YOLO is a class you've defined for handling the model
    results = model.predict(source=image, conf=0.25)
    
    # Additional check for 'results' and 'results.boxes' should be added here based on your YOLO class's return value

    for result in results:
        boxes = result.boxes
        for bbox, score, cl in zip(boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()):
            class_id = int(cl)
            input_box = np.array(bbox)

            color = (0, 100, 255) if class_id == 0 else (0, 200, 0)
            cv2.rectangle(image, (int(input_box[0]), int(input_box[1])), (int(input_box[2]), int(input_box[3])), color, 2)
            label = f"{score:.2f}"
            cv2.putText(image, label, (int(input_box[0]), int(input_box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    is_success, buffer = cv2.imencode(".jpg", image)
    if not is_success:
        return {"error": "Failed to save the image"}

    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)
    return StreamingResponse(io_buf, media_type="image/jpeg", headers={"Content-Disposition": f"inline; filename=result.jpg"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
