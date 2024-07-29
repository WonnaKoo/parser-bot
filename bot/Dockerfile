FROM python:3.9-slim

WORKDIR /app

COPY ../parser/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .. .

CMD ["python", "bot2.py"]
