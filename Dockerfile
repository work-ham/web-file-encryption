FROM python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx
RUN apt-get install ffmpeg libsm6 libxext6  -y
# Copy the rest of your project
COPY . /app

# Set the working directory
WORKDIR /app

# Install the required Python packages
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Start the application
CMD gunicorn -b :$PORT main:app
