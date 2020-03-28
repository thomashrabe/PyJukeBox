import os
import json

def read_jbdb(db_file_path: str) -> None:
    """
    Reads JukeBox db file
    :param db_file_path:
    """

    if not os.path.exists(db_file_path):
        msg = '{} does not exist!'.format(db_file_path)
        raise IOError(msg)

    with open(db_file_path, 'r') as f:
        jbdb = json.load(f)

    return jbdb

def add_new_file(db_file_path: str, code: str, new_sound_file:str) -> None:
    """
    :param db_file_path:
    :param cod:
    :param new_sound_file:
    """

    if not os.path.exists(new_sound_file):
        msg = '{} does not exist!'.format(new_sound_file)
        raise IOError(msg)

    db = read_jbdb(db_file_path)

    db[code] = new_sound_file

    with open(db_file_path, 'w') as f:
        json.dump(db, f)



