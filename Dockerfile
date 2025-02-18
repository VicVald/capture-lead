FROM python:3.12.3

WORKDIR /app

RUN pip install --no-cache-dir uv

EXPOSE 7860

COPY requirements.txt .
COPY .env .

RUN uv pip compile requirements.txt -o requirements.lock && \
    uv pip sync --system requirements.lock && \
    rm requirements.lock

COPY src/ ./src/

ENV PYTHONPATH=/app/src \
    PYTHONNUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    GRADIO_SERVER_NAME="0.0.0.0"

RUN rm -rf /root/.cache && \
    find /usr/local -type d -name __pycache__ -exec rm -r {} +

CMD ["gradio", "src/app.py"]