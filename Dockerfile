# 1. Build the Go movie-server
FROM golang:1.25.1-alpine AS builder

# Install git
RUN apk add --no-cache git bash make


# Set workdir
WORKDIR /app

# Clone movie-server repo
RUN git clone https://github.com/Danodya/movie-server.git /app/movie-server

# Set workdir
WORKDIR /app/movie-server

# Build go movie-server
RUN make
RUN go build -o /app/movie-server/movie-server


# 2. Setup python environment
FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Copy built Go binary
COPY --from=builder /app/movie-server/movie-server ./movie-server/

# Copy the Python client code
COPY ./client_app_cli ./movie-client/client_app_cli

# Install python dependencies
COPY ./requirements.txt ./movie-client
COPY ./main.py ./movie-client
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./movie-client/requirements.txt

RUN chmod +x ./movie-server/movie-server

# Expose server port
EXPOSE 8080

# Add entrypoint script
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]




