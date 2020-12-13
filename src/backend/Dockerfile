FROM alpine:3.12
RUN apk add --update --no-cache build-base bash curl python3-dev python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install fastapi
RUN pip3 install uvicorn
