import uvicorn
import cv2
import requests  # Используем requests для отправки HTTP-запросов
# import threading  # Для запуска Mock-сервера в отдельном потоке
import os
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from text_orientation import evaluate
import time  # Добавим для задержки

# Получаем пути к директориям на хосте из переменных окружения
input_dir = os.getenv('INPUT_DIR', '/app/input_images')
output_dir = os.getenv('OUTPUT_DIR', '/app/output_images')

app = FastAPI()

CLASSES = {
    0: [0],
    1: [90, cv2.ROTATE_90_COUNTERCLOCKWISE],
    2: [180, cv2.ROTATE_180],
    3: [270, cv2.ROTATE_90_CLOCKWISE]
}

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def process_path(host_input_path):
    file_name = os.path.basename(host_input_path)
    internal_input_path = os.path.join('/app/input_images', file_name)

    if not host_input_path.startswith(input_dir):
        raise HTTPException(status_code=404, detail=f"Ожидается, что путь начинается с {input_dir}")

    internal_output_path = os.path.join('/app/output_images', file_name)
    host_output_path = os.path.join(output_dir, file_name)
    return {
        "host_output_path": host_output_path,
        "internal_input_path": internal_input_path,
        "internal_output_path": internal_output_path
    }


@app.post("/predict")
async def predict_orientation(image_path: str = Form(...)):
    paths = process_path(image_path)
    try:
        internal_image_path = Path(paths['internal_input_path'])
        if not internal_image_path.exists():
            raise HTTPException(status_code=404, detail="Файл не найден")

        image = cv2.imread(str(internal_image_path))
        if image is None:
            raise HTTPException(status_code=400, detail="Не удалось прочитать изображение")

        angle_class = evaluate(img_path=str(internal_image_path))

        if angle_class == 0:
            rotated_image = image
        else:
            rotated_image = cv2.rotate(image, CLASSES[angle_class][1])

        rotated_path = paths['internal_output_path']
        cv2.imwrite(rotated_path, rotated_image)

        response = send_to_microservice_c(paths['host_output_path'], CLASSES[angle_class][0])

        return {
            "message": "Изображение успешно обработано",
            "rotated_image_path": paths['host_output_path'],
            "microservice_c_response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def send_to_microservice_c(rotated_image_path: str, angle: int):
    microservice_c_url = "http://host.docker.internal:8001/receive"

    response = requests.post(microservice_c_url, data={"rotated_image_path": rotated_image_path, 
                                                       "original_angle": angle})

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Ошибка при отправке данных в Микросервис C")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)