#!/bin/bash

docker run --publish 8080:8080 --detach -v /Users/thomas/Documents/jukebox:/jukebox  -it --entrypoint /bin/bash --name jbfprocess jbfrontend:jbf
