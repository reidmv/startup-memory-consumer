FROM python:3
ENV  PYTHONUNBUFFERED=1
COPY ./startup-memory-consumer.py /
ENTRYPOINT ["/usr/local/bin/python", "-u", "/startup-memory-consumer.py"]
