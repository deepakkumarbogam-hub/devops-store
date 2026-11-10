FROM python:3.14-alpine

WORKDIR /app

RUN apk upgrade --no-cache

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /usr/local/lib/python3.14/site-packages/pip \
              /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
              /usr/local/bin/pip \
              /usr/local/bin/pip3 \
              /usr/local/bin/pip3.14

RUN apk add --no-cache libpq \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup

COPY --chown=appuser:appgroup app.py .

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]