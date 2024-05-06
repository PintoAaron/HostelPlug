FROM python:3-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y netcat
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000