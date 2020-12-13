#!/bin/bash

# http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
JUKEBOX_SRC=$HERE/../src
JUKEBOX_BACKEND=$HERE/../src/backend
export PYTHONPATH=$JUKEBOX_SRC:$PYTHONPATH

cd $JUKEBOX_BACKEND
uvicorn main:jukeboxBackend --reload --host 0.0.0.0
