# Используйте базовый образ с Python
FROM python:3.10-slim

# Установка системных зависимостей, включая libgl1 и glib2.0 для OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Установка зависимостей проекта
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Создаем папки для входных и выходных изображений
RUN mkdir -p /app/input_images /app/output_images

# Копирование исходного кода и других необходимых файлов
COPY src /app/src
COPY model /app/model
COPY templates /app/templates

# Настройка PYTHONPATH для корректного импорта модулей
ENV PYTHONPATH=/app/src

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Устанавливаем права на папки (опционально, если нужно задать конкретные права доступа)
# RUN chmod 755 /app/input_images /app/output_images