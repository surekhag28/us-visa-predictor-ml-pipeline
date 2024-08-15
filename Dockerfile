# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11-slim


WORKDIR /app

COPY requirements.txt .

COPY setup.py .

RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install dvc[s3]  # Include appropriate DVC remote here

COPY . .

RUN mkdir -p data/raw data/processed data/transformed

CMD ["dvc", "repro"]


