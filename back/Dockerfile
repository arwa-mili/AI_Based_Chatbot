FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure logs directory exists
RUN mkdir -p /app/logs \
    && touch /app/logs/errors.log \
    && chmod -R 777 /app/logs

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run migrations and start Django dev server
CMD ["sh", "-c", "python manage.py migrate && python --noinput && make seed_languages && python manage.py runserver 0.0.0.0:8000"]