# PBL6 AI Server

## Prerequisites

1. Install RabbitMQ
```bash
docker run -d --name rabbitmq --restart unless-stopped -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
```

1. Install Python packages
```bash
pip install -r requirements-dev.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## Project Structure
```
project/
├── main.py
├── tasks/
│   ├── init.py
```

## Running the Application

1. First  Terminal - Start FastAPI:
```bash
uvicorn main:app --reload --port 8000
```

3. Second Terminal - Start Celery Worker:
```bash
celery -A main.celery worker -l INFO -P solo -E -n detect_ai_worker
```
