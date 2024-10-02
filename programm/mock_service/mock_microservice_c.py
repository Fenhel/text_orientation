import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

app_c = FastAPI()

@app_c.post("/receive")
async def receive_rotated_image(rotated_image_path: str = Form(...), original_angle: int = Form(...)):
    # Логика обработки пути до перевёрнутого изображения
    print(f"Путь до перевёрнутого изображения: {rotated_image_path}, оригинальный угол: {original_angle}")
    return JSONResponse(content={"received_rotated_image_path": rotated_image_path, 'original_angle': original_angle})

if __name__ == "__main__":
    uvicorn.run(app_c, host="0.0.0.0", port=8001, log_level="info")