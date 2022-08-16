FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code

RUN chmod +x run.sh

CMD ["./run.sh"]

EXPOSE 8000