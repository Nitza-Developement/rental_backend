FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install libmagic
RUN apt update
RUN apt install -y libmagic-dev
RUN apt install -y libpango-1.0-0 libpangoft2-1.0-0

COPY . .

# uvicorn settings.asgi:application --reload --host 0.0.0.0 --port 8000 --access-log --use-colors --log-level trace
CMD ["uvicorn", "settings.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--access-log", "--use-colors", "--log-level", "trace"]

EXPOSE 8000
