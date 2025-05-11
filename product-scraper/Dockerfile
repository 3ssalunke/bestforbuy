FROM python:3.11-slim

# Install Playwright dependencies
RUN apt-get update && apt-get install -y wget gnupg libglib2.0-0 libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libxshmfence1 libgbm-dev libx11-xcb1 && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers
RUN python -m playwright install --with-deps

COPY . .

CMD ["python", "main.py"]
