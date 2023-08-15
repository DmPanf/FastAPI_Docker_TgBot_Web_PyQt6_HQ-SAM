from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import aiofiles

app = FastAPI()

# Подключаем каталог для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Место для сохранения загруженных изображений
IMAGE_PATH = "/app/data/images/"

@app.get("/")
async def serve_root():
    """Основная страница web-клиента"""
    return FileResponse("static/index.html")
    

@app.post("/predict/")
async def upload_image(file: UploadFile = File(...)):
    """
    Загрузка изображений для обработки
    """
    try:
        # Сохраняем изображение
        file_path = IMAGE_PATH + file.filename
        async with aiofiles.open(file_path, 'wb') as buffer:
            await buffer.write(file.file.read())

        # TODO: Вызов функции для обработки изображения с помощью YOLO|SAM\HQ-SAM модели
        # processed_image = process_image_with_yolo(file_path)

        return JSONResponse(content={"filename": file.filename, "status": "uploaded and processed"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")


@app.post("/bot/")
async def get_message_from_bot(message: str):
    """
    Получение сообщений от AIOGram Telegram Bot
    """
    # TODO: Обработка полученного сообщения от Telegram Bot
    # Например, если бот получает команду /start, то можно отправить ответное сообщение (или список|JSON с перечнем доступных моделей)

    return {"message": message, "status": "received"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
