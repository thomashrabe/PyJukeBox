#!/usr/bin/env python3

import os

def jb_real_path_for_folder(a_folder: str) -> str:
    """

    @param a_folder: 
    """

    return os.path.join(ROOT_PATH, a_folder)



ROOT_PATH = '/jukebox/'
MUSIC_PATH = jb_real_path_for_folder('Music')

def jb_music_path_for_folder(a_folder: str) -> str:
    """

    @param a_folder: 
    """

    return os.path.join(MUSIC_PATH, a_folder)
