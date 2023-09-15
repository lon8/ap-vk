FROM python:3.9

WORKDIR /app
COPY ./vk-service /app

RUN pip install fastapi uvicorn vk_api requests

CMD ["uvicorn", "ap-gateway.main:app", "--host", "0.0.0.0", "--port", "80"]