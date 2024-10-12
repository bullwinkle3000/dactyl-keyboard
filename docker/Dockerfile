FROM python:3.10.8-slim-bullseye

RUN apt update && \
    apt install -y git

RUN pip install \
        cadquery-ocp==7.6.3a0 \
        git+https://github.com/CadQuery/cadquery.git \
        dataclasses-json \
        numpy \
        scipy \
        solidpython

WORKDIR /app
