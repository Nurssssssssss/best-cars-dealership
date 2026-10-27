FROM node:20-alpine AS frontend
WORKDIR /frontend
COPY server/frontend/package*.json ./
RUN npm install
COPY server/frontend/ ./
RUN npm run build
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DJANGO_SERVE_REACT=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server/ ./server/
COPY --from=frontend /frontend/dist/ ./server/frontend/dist/
WORKDIR /app/server
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh","-c","python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
