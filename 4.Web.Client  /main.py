from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Optional
from pydantic import BaseModel
import glob
import os
#import torch
#torch.cuda.is_available = lambda : False  # принудительно использовать только CPU для PyTorch

default_mdl_path = './models/'  # Путь по умолчанию, где хранятся модели

app = FastAPI(title="Screening System API", version="0.1.0", debug=True)  # Инициализация FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_latest_model(path):  # Функция для выбора самой последней модели
    list_of_files = glob.glob(f'{path}*.pt')
    if not list_of_files:
        return None  # Ни одного файла модели не найдено
    latest_model = max(list_of_files, key=os.path.getctime)  # Выбираем самый свежий файл
    print(f'♻️  Latest Model: {latest_model}')
    return latest_model


def draw_boxes(image: np.ndarray, results: list) -> np.ndarray:
    for result in results:
        boxes = result.boxes
        for bbox, score, cl in zip(boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()):
            class_id = int(cl)
            input_box = np.array(bbox)
            color = (0, 100, 255) if class_id == 0 else (0, 200, 0)
            cv2.rectangle(image, (int(input_box[0]), int(input_box[1])), (int(input_box[2]), int(input_box[3])), color, 2)
            label = f"{score:.2f}"
            cv2.putText(image, label, (int(input_box[0]), int(input_box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return image


# Добавление статических файлов
app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    ## return templates.TemplateResponse("index.html", {"request": request})
    #model_files_response = list_models()
    #model_files = model_files_response.body  # Вытащить содержимое JSONResponse
    #model_files_dict = json.loads(model_files.decode())  # Декодировать и конвертировать в словарь
    model_files = list_models()  # это словарь
    print(f"\n🛒 Доступные модели: {model_files['Models']}")
    return templates.TemplateResponse("index.html", {"request": request, "models": model_files['Models']})


@app.get('/info')
def read_root():
    return {'Project 2023': '🩻 Screening System - система досмотра СРК "Express Inspection" [г. Москва, 2023 г.]'}


@app.get('/models')
def list_models():
    models_dir = "models"
    models = []

    for filename in os.listdir(models_dir):
        if filename.endswith(".h5") or filename.endswith(".pt"):  # Расширения файлов моделей
            models.append(filename)
    #return JSONResponse(content={"Models": models})
    return {"Models": models}


@app.post('/predict')
async def predict(file: UploadFile = File(...), mdl_name: Optional[str] = Form(None)):
    print("... Received model name:", mdl_name) # для отладки !!!
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
        print(f'⚖️  Selected Model: {selected_model}')
    else:
        selected_model = get_latest_model(default_mdl_path)

    if selected_model is None:
        return {"error": "No model files found"}

    # Загружаем модель в память
    model = YOLO(selected_model) # if selected_model else None
    results = model.predict(source=image, conf=0.25)
    image = draw_boxes(image, results)

    is_success, buffer = cv2.imencode(".jpg", image)
    if not is_success:
        return {"error": "Failed to save the image"}

    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)
    return StreamingResponse(io_buf, media_type="image/jpeg", headers={"Content-Disposition": f"inline; filename=result.jpg"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
