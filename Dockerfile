FROM python:3.9-slim AS builder 

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


FROM python:3.9-slim

RUN apt-get update

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY ./src/jizt ./jizt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

RUN python3 -c 'import nltk; nltk.download("punkt")'

CMD ["uvicorn", "jizt.main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "80"]
