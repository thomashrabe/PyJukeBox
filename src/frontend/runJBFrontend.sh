#!/bin/bash

docker run --publish 8080:8080 --detach -v /Users/thomas/Documents/jukebox:/jukebox  -it --entrypoint /jukebox/src/frontend/runVueServer.sh --name jbfprocess jbfrontend:jbf
