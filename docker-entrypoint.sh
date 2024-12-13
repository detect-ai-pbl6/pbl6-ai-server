#!/bin/bash

echo "Starting server & celery server"
uvicorn main:app --host 0.0.0.0 --port 80 &
celery -A main.celery worker -l INFO -P solo -E -n detect_ai_worker
