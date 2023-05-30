# Base image
FROM python:3.10

WORKDIR /Back/

COPY ./ /Back/
COPY ./requirements.txt /Back/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000 
EXPOSE 8001 
EXPOSE 8002

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker \ 
    --bind 0.0.0.0:8000 \
    --bind 0.0.0.0:8001 \
    --bind 0.0.0.0:8002