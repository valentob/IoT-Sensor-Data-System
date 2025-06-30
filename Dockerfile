
FROM python:3.8-slim


WORKDIR /app


COPY sensor.py .


RUN pip install requests


CMD ["python", "sensor.py"]
