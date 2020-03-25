#!/bin/bash

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
JUKEBOX_SRC=$HERE/src
export PYTHONPATH=$JUKEBOX_SRC:$PYTHONPATH

$JUKEBOX_SRC/jukebox/jukebox.py
