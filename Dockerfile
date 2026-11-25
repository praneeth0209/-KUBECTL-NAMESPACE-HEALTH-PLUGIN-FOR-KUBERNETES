FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Flask application port
EXPOSE 5000

# Start the production-style web server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
