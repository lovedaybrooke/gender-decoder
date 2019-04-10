FROM python:3.7-alpine

RUN pip install pipenv
WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY ./Pipfile* /app/
RUN ls -l /app
RUN pipenv install

COPY . /app

EXPOSE 5000/tcp
ENTRYPOINT ["pipenv", "run"]
CMD ["python", "runsite.py"]
