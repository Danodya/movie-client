#!/bin/bash
set -e

echo "Starting movie server..."
./movie-server/movie-server &  # Run in background

sleep 5

python movie-client/main.py -y "$@"
