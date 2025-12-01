FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /punchpoint

# Install build deps first (keeps image small)
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

copy . /punchpoint

EXPOSE 5000

# Use Gunicorn to serve the Flask app (main.py defines "app")
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]