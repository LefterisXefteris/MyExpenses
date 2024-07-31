FROM python:3.9-slim

# Install Java
RUN apt-get update && apt-get install -y default-jdk

WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]