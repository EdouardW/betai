#/bin/bash

export PORT=8080

gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --reload betai_flask:app
