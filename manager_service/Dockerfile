FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements ./requirements
COPY poetry.lock pyproject.toml .
COPY entrypoint.sh .

RUN pip3 install poetry
RUN poetry install

COPY . /code

ENTRYPOINT ["sh", "/code/entrypoint.sh"]