# Base image
FROM --platform=linux/amd64 python:3.10

WORKDIR /Back/

COPY ./requirements.txt /Back/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /Back/

EXPOSE 8003 
EXPOSE 8004 
EXPOSE 8005

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker \ 
    --bind 127.0.0.1:8003 \
    --bind 127.0.0.1:8004 \
    --bind 127.0.0.1:8005