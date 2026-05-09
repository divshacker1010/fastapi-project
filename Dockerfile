FROM python:3.11-slim

WORKDIR /app

COPY blog/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "8000"]
