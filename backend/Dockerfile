FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requeriments.txt
EXPOSE 8000

CMD ["fastapi", "run", "app.py"]
