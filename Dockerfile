# Base image
FROM python:3.10

WORKDIR /Back/

COPY ./ /Back/
COPY ./requirements.txt /Back/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000 8001 8002

CMD uvicorn --host 0.0.0.0 --port 8000 --workers 4 main:app && \
    uvicorn --host 0.0.0.0 --port 8001 --workers 4 main:app && \
    uvicorn --host 0.0.0.0 --port 8002 --workers 4 main:app