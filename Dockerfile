# This is a multi-stage Dockerfile that builds a Go movie-server and sets up a Python client environment.
# Stage 1: Build the Go movie-server
FROM golang:1.25.1-alpine AS builder

# Install git and make, clone the repo, build the server
RUN apk add --no-cache git make \
 && git clone https://github.com/Danodya/movie-server.git /app/movie-server \
 && cd /app/movie-server \
 && make \
 && go build -o /app/movie-server/movie-server


# Stage 2: Setup python environment
FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Copy built Go binary
COPY --from=builder /app/movie-server/movie-server ./movie-server/

# Copy the Python client code
COPY ./client_app_cli ./movie-client/client_app_cli

# Install Python dependencies
COPY ./requirements.txt ./movie-client
COPY ./main.py ./movie-client
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./movie-client/requirements.txt

RUN chmod +x ./movie-server/movie-server

# Add entrypoint script
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Expose server port
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]




