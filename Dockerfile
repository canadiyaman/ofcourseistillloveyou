FROM python:3.13
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install && \
    apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y git \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /base
COPY requirements.txt /base/
COPY .env /base/.env
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /base/
