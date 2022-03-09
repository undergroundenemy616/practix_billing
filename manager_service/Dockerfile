FROM python:3.10.0-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY poetry.lock pyproject.toml ./
COPY entrypoint.sh ./

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN python3 -m grpc_tools.protoc -I ./auth_grpc --python_out=./auth_grpc \
         --grpc_python_out=./auth_grpc ./auth_grpc/auth.proto

COPY . /code

