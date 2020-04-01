FROM python:3.8-alpine
ADD . /code
WORKDIR /code
ENV APP_HOME=/code
COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt
CMD python3 app.py
