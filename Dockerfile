FROM nikolaik/python-nodejs:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y unrar-free zip
RUN pip install --upgrade pip

RUN mkdir /code
RUN mkdir /comics
WORKDIR /code
COPY . /code/
# Install requirements
RUN pip install -r requirements.txt
