#!/bin/bash

# http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
JUKEBOX_SRC=$HERE/../src
export PYTHONPATH=$JUKEBOX_SRC:$PYTHONPATH

$JUKEBOX_SRC/jukebox/jukebox.py --db /home/pi/.jukebox/db.jbdb
