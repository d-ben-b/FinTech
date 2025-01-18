# Use official Python base image
FROM python:3.9-slim

# Prevent Python from writing pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port 8000 for Django
# EXPOSE 8000

# # Run the Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
