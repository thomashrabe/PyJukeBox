#!/bin/bash

docker run --publish 8000:8080 --detach -v /Users/thomas/Documents/jukebox:/jukebox  -it --entrypoint /bin/bash --name jbbprocess jbbackend:jbb