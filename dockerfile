# Dockerfile

# Use a base image with Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies needed for Chrome (gnupg is important here)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    --no-install-recommends

# --- START: CORRECTED CHROME INSTALLATION ---

# 1. Download the key and store it in the keyring directory
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg

# 2. Add the Chrome repository, pointing to the key we just saved
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# 3. Update apt and install Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# --- END: CORRECTED CHROME INSTALLATION ---

# Copy requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- NEW LINE: Add this to upgrade pip ---
    RUN pip install --upgrade pip


# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["uvicorn", "scraper_api:app", "--host", "0.0.0.0", "--port", "8000"]