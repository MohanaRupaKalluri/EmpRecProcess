# Works on Koyeb, Hugging Face Spaces (Docker SDK), Railway, Fly.io and Render.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# MONGO_URI and SECRET_KEY must be provided as environment variables / secrets.
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 wsgi:app
