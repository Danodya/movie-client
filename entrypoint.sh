#!/bin/bash
set -e

echo "Starting movie server..."
./movie-server/movie-server &  # Run in background

sleep 5


# Ensure both arguments (-y and -s) are provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: entrypoint.sh -y <year(s)> -s <search_term> [--count-only]"
  exit 1
fi

python movie-client/main.py "$@"
