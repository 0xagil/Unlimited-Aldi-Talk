# Dockerfile for AldiTalk Refresher

# 1. Use the official Playwright Python image
# This image comes with Python and all necessary browser dependencies pre-installed.
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
# This step is done separately to leverage Docker's layer caching.
# The dependencies will only be re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Install the browser binaries required by Playwright
# This ensures that Chromium is available inside the container.
RUN playwright install chromium

# 5. Copy the rest of the application code into the container
COPY . .

# 6. Set the command to run the application
# This will execute the main.py script when the container starts.
CMD ["python", "main.py"]
