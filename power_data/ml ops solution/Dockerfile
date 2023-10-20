FROM python:3.11-slim

WORKDIR .

ARG APP_DIR=.
COPY "${APP_DIR}"/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pandas

ARG APP_DIR=.
COPY "${APP_DIR}"/. .

EXPOSE 80

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]