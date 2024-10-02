# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY mock_microservice_c.py .

# Запускаем Mock-сервис
CMD ["uvicorn", "mock_microservice_c:app_c", "--host", "0.0.0.0", "--port", "8001"]