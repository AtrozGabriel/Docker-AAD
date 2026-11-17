
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home --uid 10001 appuser

USER appuser

ENV PORTA=8080
ENV LOG_LEVEL=INFO

EXPOSE 8080

CMD ["python", "-u", "app.py"]