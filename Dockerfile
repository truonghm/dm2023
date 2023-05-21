FROM python:3.10.10

WORKDIR /project/

COPY ./project .
COPY ./requirements-project.txt .

RUN pip install --user --upgrade pip
RUN pip install -r requirements-project.txt --no-cache-dir