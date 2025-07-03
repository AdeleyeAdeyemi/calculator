
FROM python:3.10-slim

WORKDIR /app

COPY app.py .
COPY Scores.txt .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8777

CMD ["python", "app.py"]
