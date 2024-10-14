FROM python:3.11.9-alpine
ENV PYTHONBUFFERED=1
WORKDIR /usr/src/
COPY ./requirements.txt .
RUN RUN pip install --upgrade pip && pip install -r requirements.txt && rm -rf ~/.cache/pip