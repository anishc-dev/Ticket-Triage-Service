FROM python:3.10
WORKDIR /app
COPY docker/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]