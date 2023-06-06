# Base image
FROM --platform=linux/amd64 python:3.10

WORKDIR /Back/

COPY ./requirements.txt /Back/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /Back/

EXPOSE 8000 
EXPOSE 8001 
EXPOSE 8002

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker \ 
    --bind 0.0.0.0:8000 \
    --bind 0.0.0.0:8001 \
    --bind 0.0.0.0:8002