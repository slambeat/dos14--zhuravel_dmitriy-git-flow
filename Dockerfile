FROM python:3.11-buster

ARG APP_FOLDER=/home/bank/bank_git

RUN pip install poetry && useradd -d /home/bank -U -m -u 1111 bank && mkdir $APP_FOLDER

WORKDIR $APP_FOLDER

COPY --chown=bank:bank . .

USER root

RUN chmod 777 $APP_FOLDER

USER bank

RUN poetry install

ENTRYPOINT ["poetry", "run"]

CMD ["python", "main_hw19.py"]
