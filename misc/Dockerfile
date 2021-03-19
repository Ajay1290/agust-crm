FROM python:3.7.5-slim-buster

RUN apt-get update && apt-get install -qq -y build-essential libpq-dev --no-install-recommends

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV INSTALL_PATH .
RUN mkdir -p $INSTALL_PATH

COPY . /website

WORKDIR /website

# COPY req.txt /website/req.txt
# RUN pip install -r req.txt

RUN ls

CMD cd "/website" && gunicorn -c "python:config.gunicorn" "manager:create_app()"