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

# No environment variables required: the app ships with an embedded demo database.
# Set MONGO_URI (+ optional SECRET_KEY) only to use a real MongoDB.
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 wsgi:app
