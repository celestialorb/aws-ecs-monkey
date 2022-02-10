FROM python:3-slim

RUN mkdir -p /opt/monkey
COPY src /opt/monkey
COPY requirements.txt /opt/monkey/requirements.txt
RUN pip install -r /opt/monkey/requirements.txt

WORKDIR /opt/monkey
ENTRYPOINT [ "python", "/opt/monkey/main.py" ]
