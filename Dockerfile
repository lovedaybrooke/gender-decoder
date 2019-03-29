FROM python:3

RUN pip install pipenv
WORKDIR /app

COPY ./Pipfile* /app/
RUN ls -l /app
RUN pipenv install

COPY . /app

EXPOSE 5000/tcp
ENTRYPOINT ["pipenv", "run"]
CMD ["python", "runsite.py"]
