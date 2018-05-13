FROM python:3.6

# Install required packages.
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    wget \
    unrar-free \
    gettext \
    libxmlsec1-dev \
  && rm -rf /var/lib/apt/lists/*

# Install node 8 and yarn globally.
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update && apt-get install -y nodejs
RUN npm install -g yarn

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
RUN mkdir /comics
RUN mkdir /code
WORKDIR /code

# Install dependencies
COPY requirements/local.txt requirements.txt
RUN pip install -r requirements.txt
RUN yarn install

# Copy the rest of the application's code
COPY . /code
