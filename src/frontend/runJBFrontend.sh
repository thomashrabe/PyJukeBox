#!/bin/bash

docker run --publish 8080:8080 -dit -v /Users/thomas/Documents/jukebox:/jukebox --entrypoint /jukebox/src/frontend/runVueServer.sh --name jbfprocess jbfrontend:jbf
