FROM python:3.10 

WORKDIR /code 

COPY . /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi
RUN poetry run pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN poetry run pip install fasttext
RUN mkdir /code/app/utils/artifacts

RUN curl -k -L -s https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin > /code/app/utils/artifacts/lid.176.bin

RUN chmod +x /code/*.sh

CMD ["/code/run.sh"]