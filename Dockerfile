FROM python:3.11

RUN mkdir /app

RUN pip install poetry

COPY templates /app/templates
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.toml
WORKDIR /app

RUN poetry config virtualenvs.create false && poetry install



COPY go.py /app/go.py
CMD ["python", "go.py"]