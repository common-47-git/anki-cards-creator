FROM python:3.13-slim

WORKDIR /app

# Copy only requirements.txt first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Default command
CMD ["python", "main.py"]
