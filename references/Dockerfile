FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r backend/requirements.txt

COPY . .

CMD ["uvicorn", "start:app", "--host", "0.0.0.0", "--port", "8000"]
