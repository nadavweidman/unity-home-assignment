# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to ensure the Python output is sent straight to the terminal (not buffered)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory for the app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 3000

# Run the command to start the Flask application
CMD ["python", "frontend.py"]
