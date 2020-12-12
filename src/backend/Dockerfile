FROM alpine:3.12
RUN apk add --update --no-cache build-base python3-dev python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip && ln -sf pip3 /usr/bin/pip
RUN pip install fastapi
RUN pip install uvicorn

