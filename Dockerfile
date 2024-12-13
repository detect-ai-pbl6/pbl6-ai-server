FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

COPY . /app

RUN chmod +x docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["./docker-entrypoint.sh"]
