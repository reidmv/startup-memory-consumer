FROM python:3
COPY ./startup-memory-consumer.py /
CMD /usr/local/bin/python /startup-memory-consumer.py
