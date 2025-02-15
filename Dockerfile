# Use the official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install vim and other necessary dependencies
RUN apt-get update && apt-get install -y \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install any additional Python dependencies (if needed)
RUN pip install --no-cache-dir BeautifulSoup4
RUN pip install --no-cache-dir requests

# Copy your current directory contents into the container (if necessary)
COPY . /app

# Expose the port (if you're running a web server or app)
# EXPOSE 5000

# Set the default command to run when the container starts (if necessary)
# CMD ["python", "your-script.py"]

# Start an interactive shell by default
CMD ["bash"]
