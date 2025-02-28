# Use the official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Install additional system dependencies for Tesseract and Poppler (for PDF handling)
# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     poppler-utils \
#     && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY . .

RUN chmod +x /app/analyzer.py

# Command to run the program
CMD ["python", "analyzer.py"]
