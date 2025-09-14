#!/bin/bash
set -e

echo "Starting movie server..."
./movie-server/movie-server &  # Run in background

sleep 5

echo "Running movie client..."
python movie-client/main.py -y "$@"
