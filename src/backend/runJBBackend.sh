#!/bin/bash

docker run --publish 8000:8000 -dit -v /Users/thomas/Documents/jukebox:/jukebox  --entrypoint /jukebox/bin/runBackend.sh --name jbbprocess jbbackend:jbb