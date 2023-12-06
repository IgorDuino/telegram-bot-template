FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install poetry
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD [ "python", "main.py"]