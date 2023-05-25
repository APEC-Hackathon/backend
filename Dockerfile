FROM python:3.10 

WORKDIR /code 

COPY . /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

RUN chmod +x /code/*.sh

CMD ["/code/run.sh"]