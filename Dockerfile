FROM lambci/lambda:python3.7
MAINTAINER tech@21buttons.com

USER root

ENV APP_DIR /var/task

WORKDIR $APP_DIR
# scraping
COPY requirements-scraper.txt .
COPY bin ./bin
COPY lib ./lib

RUN mkdir -p $APP_DIR/lib
RUN pip3 install -r requirements-scraper.txt -t /var/task/lib

# ner
# COPY requirements-ner.txt .
# # COPY bin ./bin
# COPY lib ./lib

# RUN mkdir -p $APP_DIR/lib
# RUN pip3 install -r requirements-ner.txt -t /var/task/lib