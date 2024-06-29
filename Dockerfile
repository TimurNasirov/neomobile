FROM python:3.11-slim

RUN mkdir container
ADD . /container/
RUN pip install -r requirements.txt

CMD python main.py