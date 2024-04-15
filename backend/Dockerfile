FROM alpine:3.19.1

RUN mkdir /server
RUN mkdir /server/data
RUN apk update
RUN apk add python3 py3-pip gcc python3-dev musl-dev linux-headers
WORKDIR /server
RUN python3 -m venv ./venv
ENV PATH="/server/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./objst.py .

ENTRYPOINT python3 objst.py