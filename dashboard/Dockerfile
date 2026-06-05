FROM python:3.12-slim

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends docker-cli curl 2>&1 | tail -3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "--timeout", "30", "app:app"]
