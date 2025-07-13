FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies for Node, postgres
RUN apt-get update && apt-get install -y curl git build-essential postgresql-client

# Install Node.js LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install AppWright
RUN npm install -g appwright

# Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend ./backend
COPY alembic.ini ./
COPY alembic ./alembic
COPY .env .env
COPY entrypoint.sh ./entrypoint.sh
COPY backend/wait_for_postgres.sh ./wait_for_postgres.sh

RUN chmod +x entrypoint.sh wait_for_postgres.sh
ENTRYPOINT ["./entrypoint.sh"]

