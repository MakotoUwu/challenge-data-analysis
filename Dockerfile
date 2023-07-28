# Use the latest official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy current directory files to /app in container
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Open port 80 for the app
EXPOSE 80

# Run the command to start uWSGI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
