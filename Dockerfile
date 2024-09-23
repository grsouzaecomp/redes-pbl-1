FROM python:3.9-slim

WORKDIR /app

COPY . .

EXPOSE 12345

CMD ["python", "server.py"]